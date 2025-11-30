# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the Europa Universalis V game data directory, primarily used for modding. The game uses Paradox's Clausewitz engine with the Jomini framework. All game content is defined through declarative text files using Paradox's scripting language.

## Directory Structure

- `game/in_game/common/` - Core game definitions (110+ categories: buildings, events, laws, religions, etc.)
- `game/in_game/events/` - Event scripts organized by namespace
- `game/in_game/gui/` - GUI layout definitions (.gui files)
- `game/in_game/localization/` - Multi-language text strings
- `game/in_game/gfx/` - Graphics assets (models, textures, particles)
- `game/mod/` - Custom mod directory
- `clausewitz/` - Engine assets
- `jomini/` - Framework assets

## Research Documentation

The `.claude/docs/` directory contains detailed research findings from codebase exploration. These are searchable reference documents for future development:

| Document | Contents |
|----------|----------|
| `historical-data-tracking.md` | On_action hooks, variable storage, 60-slot rotation pattern for historical data |
| `gui-graph-system.md` | Plotlines, axes, multi-line graphs, legends, tooltips |
| `engineering-lessons.md` | **READ FIRST** - Critical gotchas, limitations, and patterns learned from implementation |

**When exploring new systems**, save findings to `.claude/docs/<topic>.md` for future reference.

## File Formats

### Paradox Script Files (.txt)
- UTF-8 with BOM encoding
- Key-value pairs with nested blocks using `{}`
- Comments start with `#`
- Numerical prefixes for load order (e.g., `00_generic.txt`, `01_specific.txt`)

### Scripted Effects/Triggers
Arguments use `$variable$` syntax for text replacement:
```
my_effect = {
    $target$ = { add_prestige = $value$ }
}
# Usage: my_effect = { target = scope:receiver value = 10 }
```

**Important**: When using `custom_description`, use a different key than the effect/trigger name:
```
# Wrong:
my_effect = { custom_description = { text = my_effect } }
# Correct:
my_effect = { custom_description = { text = my_effect_text } }
```

### Events
- Require namespace declaration at file top: `namespace = event_namespace`
- Event IDs: `namespace.number` (number 1-9999, must be unique)
- Event types: `country_event`, `location_event`, `unit_event`, `exploration_event`, `age_event`
- Structure: trigger → immediate → options → after

### Tests
Location: `game/in_game/common/tests/`
```
test_name = {
    year = 1346
    success = { <triggers> }
    failure = { <triggers> }
    end_year = 1360
    fail_on_end_year = yes
    success_effect = { test_log = "message" }
    failure_effect = { test_log = "message" }
}
```

## Key Concepts

### Scopes
Scripts operate within scopes (country, location, character, etc.). Use scope changers to target different entities:
- `root` - The original scope
- `scope:name` - Named saved scope
- `prev` - Previous scope in chain

### Modifiers
- `modifier` - Scaled by building level/goods access
- `raw_modifier` - Not scaled
- `capital_modifier` - Applied only in capital
- `country_modifier` - Applied to the whole country

### AI Behavior
- `ai_chance` - MTTH-style likelihood calculation
- `ai_will_select` - Script math override for event options

## Documentation

Each `common/` subdirectory contains a `readme.txt` documenting:
- Available attributes and their types
- Required vs optional fields
- Trigger/effect scopes
- Usage examples

## Modding Workflow

1. Create mod folder in `game/mod/`
2. Mirror the `game/in_game/` structure for files to override
3. Use unique identifiers to avoid conflicts with base game
4. Test using the in-game test framework
5. Check game error.log for script validation errors

## Common Directories Reference

| Directory | Purpose |
|-----------|---------|
| `advances/` | Technology/advancement tree |
| `building_types/` | Building definitions with production methods |
| `casus_belli/` | War justification types |
| `disasters/` | Disaster event chains |
| `estates/` | Estate system definitions |
| `government_types/` | Government forms and reforms |
| `laws/` | Country law definitions |
| `on_action/` | Event callback hooks |
| `scripted_effects/` | Reusable effect macros |
| `scripted_triggers/` | Reusable condition macros |
| `situations/` | Dynamic situation definitions |
| `traits/` | Character trait definitions |

## Mod Structure

**CRITICAL**: Mods load from `Documents/Paradox Interactive/Europa Universalis V/mod/`, NOT `game/mod/`.

### Required Folder Structure
```
mod_name/
├── .metadata/
│   └── metadata.json    # ALL fields below required!
└── in_game/             # Must use in_game/ wrapper
    ├── common/
    ├── gui/
    ├── gfx/
    └── localization/
```

### Required metadata.json (ALL fields mandatory)
```json
{
    "name": "Mod Name",
    "id": "",
    "version": "1.0.0",
    "supported_game_version": "1.0.0",
    "short_description": "Description",
    "tags": ["Utilities"],
    "relationships": [],
    "game_custom_data": { "multiplayer_synchronized": false }
}
```
- `id`: Empty string (game assigns)
- `tags`: Required array, not optional
- `relationships`: Required even if empty
- `game_custom_data`: Required with `multiplayer_synchronized`

### Development Workflow (Windows)
Use junctions to edit in `game/mod/` while game loads from Documents:
```powershell
New-Item -ItemType Junction -Path "$env:USERPROFILE\Documents\Paradox Interactive\Europa Universalis V\mod\<mod>" -Target "<steam>\game\mod\<mod>"
```

### Error Log Location
`Documents/Paradox Interactive/Europa Universalis V/logs/error.log`

## GUI Tooltip Patterns

### Modifier Breakdowns
To display a modifier value with its sources breakdown:
```
# Header showing total value
TooltipListBase = {
    visible = "[<condition>]"
    TooltipManualTableField = {
        text_single = { text = "LABEL_KEY" }
        expand = {}
        text_single = { raw_text = "[Player.GetModifierValue('modifier_name')|%0]" }
    }
}

# Breakdown list showing all sources
TooltipStringPairList = {
    visible = "[<condition>]"
    datacontext = "[Player.GetModifierTooltipContext('modifier_name')]"
    textcontext = "[CountryModifierWrap.GetTooltip]"
}
```

### Estate-Specific Conditionals
Since there's no dynamic estate key accessor, use conditional blocks per estate type:
```
visible = "[And(Not(Estate.GetType.IsAlwaysLoyal), ObjectsEqual(Player.GetGovernment.GetEstateFromKey('nobles_estate').GetType, Estate.GetType))]"
```

Estate keys: `nobles_estate`, `clergy_estate`, `burghers_estate`, `peasants_estate`, `dhimmi_estate`, `tribes_estate`, `cossacks_estate`

### Key Tooltip Templates
| Template | Purpose |
|----------|---------|
| `TooltipListBase` | Container for table-style rows |
| `TooltipManualTableField` | Label + value row |
| `TooltipStringPairList` | List from string pair data |
| `TooltipTextBlock` | Simple text block |
| `CountryModifier_tooltip` | Standard modifier breakdown tooltip |

### Useful GUI Functions
- `Player.GetModifierValue('modifier_name')` - Get current modifier value
- `Player.GetModifierTooltipContext('modifier_name')` - Get breakdown context for tooltip
- `CountryModifierWrap.GetTooltip` - Extract tooltip string pairs from context
- `Estate.GetType.IsAlwaysLoyal` - Check if estate is crown (always loyal)

## Custom GUI Windows

**Working References:**
- [EU5-Cheat-Menu](https://github.com/3DMXM/EU5-Cheat-Menu) - Button in message_log.gui override
- [EU5-Minesweeper](https://github.com/CountCristo/Eu5-modtemplate) - Button in right_panel.gui override

### CRITICAL: Window Creation Pattern

**Windows MUST be:**
1. Registered in `gui/scripted_widgets/` folder
2. Created/destroyed using console commands
3. Opened via buttons embedded in vanilla file overrides

### Step 1: Register Window in scripted_widgets
Create `in_game/gui/scripted_widgets/your_windows.txt`:
```
gui/your_window.gui = your_window_name
```

### Step 2: Override Vanilla GUI to Add Button
Override `message_log.gui` or `panels/right_panel/right_panel.gui` to embed your button:
```
# In your override of message_log.gui, add button to messages_toggle_button type:
button = {
    parentanchor = right|vcenter
    position = { -35 0 }
    size = { 30 30 }

    # Toggle pattern: close if open, create if closed
    onclick = "[ExecuteConsoleCommand( Select_CString( GetVariableSystem.Exists('my_window_open'), 'gui.ClearWidgets my_window', 'gui.createwidget gui/my_window.gui my_window' ) )]"
    onclick = "[GetVariableSystem.Toggle('my_window_open')]"

    icon = {
        texture = "gfx/interface/component_tiles/hud_corners/circle_progress_bg.dds"
        size = {100% 100%}
    }
    icon = {
        size = { 75% 75% }
        parentanchor = center
        texture = "gfx/interface/icons/flat_icons/tabicons/economy.dds"
    }
    tooltip = "Open My Window"
}
```

### Step 3: Window Definition
```
window = {
    name = "my_window"
    parentanchor = center
    size = { 800 600 }
    layer = windows_layer
    movable = yes

    # NO visible condition - window is created/destroyed by console commands

    using = Window_Background_Illustration  # or bg_window_default_alt

    vbox = {
        # ... content ...

        # Close button
        button = {
            onclick = "[ExecuteConsoleCommand('gui.ClearWidgets my_window')]"
            onclick = "[GetVariableSystem.Clear('my_window_open')]"
            # ...
        }
    }
}
```

### Console Commands
- `gui.createwidget gui/file.gui window_name` - Create window
- `gui.ClearWidgets window_name` - Destroy window
- `Select_CString(condition, 'if_true', 'if_false')` - Conditional string selection

### Valid Button Types
- `button` - Basic button with texture
- `button_main_tab_alt` - Tab button (use with blockoverride "text")
- `button_regular_diamond` - Styled button
- `button_close_alt` - Close button (use blockoverride "close_onclick")

**INVALID types** (will cause errors):
- `button_tab`, `button_tab_small`, `button_icon_close`

### Tabs (within windows)
```
button_main_tab_alt = {
    down = "[GetVariableSystem.Exists('tab_2')]"
    onclick = "[GetVariableSystem.Set('tab_2', 'yes')]"
    blockoverride "on_action_left" {}
    blockoverride "text" { text = "TAB_NAME" }
}
```

### Plotlines (LIMITATION: No custom data)
`plotpoints` only accepts built-in functions:
- `Player.GetHistoricalTaxBase`, `Player.GetHistoricalPopulation`
- Cannot construct from variables - use dot overlays for custom data

### On_Action Hooks
```
monthly_country_pulse = { on_actions = { my_action } }
my_action = { trigger = { is_ai = no } effect = { ... } }
```
**Always filter `is_ai = no`** - fires for ALL countries every month.

### Key GUI Files
- `gui/shared/plotlines.gui` - Graph templates
- `gui/shared/standard_types.gui` - Basic types
- `main_menu/gui/shared/main_menu_buttons.gui` - Button type definitions
- `gui/message_log.gui` - Good override target for adding buttons

### Layout Quick Reference
- Containers: `vbox`, `hbox`, `widget`, `scrollbox`
- Sizing: `layoutpolicy_horizontal = expanding`, `size = { 100% 50 }`
- Position: `parentanchor = center`, `margin = { 10 10 }`
- Common backgrounds: `using = bg_window_default_alt`, `using = bg_age_event_inner`

## Python Code Generators

**No runtime** - Python generates `.txt` files at dev time. Game only loads generated output.

### When to Use
- Repetitive patterns (grids, state machines, 60-slot rotations)
- No loops in Paradox script - Python fills the gap

### Pattern: N-slot rotation (historical data)
```python
for i in range(59, 0, -1):
    print(f"set_variable = {{ name = data_{i} value = var:data_{i-1} }}")
print(f"set_variable = {{ name = data_0 value = current_value }}")
```

### Workflow
1. Write generator in `scripts/`
2. Run → output to `in_game/common/scripted_effects/`
3. Game loads generated `.txt`

## Critical Limitations (READ FIRST)

### Variables
- **No dynamic names**: `var:data_$i$` does NOT work
- **No loops**: Use Python generators
- **Initialize before use**: Uninitialized = errors

### GUI
- **plotpoints**: Only built-in functions, cannot construct from variables
- **No dynamic positioning**: Use visibility bands instead
- **Tooltips on plotline**: Not supported - overlay dot widgets

### Localization
- **UTF-8 BOM required**: `encoding='utf-8-sig'` in Python
- Without BOM: Silent failure, text won't load

### Performance
- **Monthly pulse**: Fires for ALL countries - always filter `is_ai = no`

See `.claude/docs/engineering-lessons.md` for detailed patterns.