# EU5 Modding - Engineering Lessons

Critical knowledge for implementation. **Read before coding.**

---

## 1. Mod Loading (CRITICAL)

### Location
Mods load from **Documents**, not game directory:
```
Documents/Paradox Interactive/Europa Universalis V/mod/<mod_name>/
```

### Required Structure
```
mod_name/
├── .metadata/metadata.json   # ALL fields required
└── in_game/                  # Content wrapper
    ├── common/
    ├── gui/
    └── localization/
```

### metadata.json - ALL FIELDS REQUIRED
```json
{
    "name": "Name",
    "id": "",
    "version": "1.0.0",
    "supported_game_version": "1.0.0",
    "short_description": "Desc",
    "tags": ["Utilities"],
    "relationships": [],
    "game_custom_data": { "multiplayer_synchronized": false }
}
```
- `id`: Empty string (game assigns)
- Missing ANY field = mod won't load (check error.log)

### Development Workflow
Use Windows junctions (not WSL symlinks):
```powershell
New-Item -ItemType Junction -Path "Documents\..\mod\<name>" -Target "game\mod\<name>"
```

---

## 2. Plotline Widget Limitations

**Cannot use custom variable data in plotlines.**

`plotpoints` only accepts built-in functions:
- `Player.GetHistoricalTaxBase`
- `Player.GetHistoricalPopulation`
- `EconomyView.GetRecentBalance`

### Workaround: Dot Overlays
Fixed-position widgets with tooltips at yearly intervals:
```
widget = {
    position = { 80% 50% }  # Fixed X for "1 year ago"
    tooltip = "[Player.Var('data_12')]"
}
```

---

## 3. Variable System

### No Dynamic Names
```
# DOES NOT WORK:
set_variable = { name = data_$i$ value = 0 }

# Must hardcode each:
set_variable = { name = data_0 value = 0 }
set_variable = { name = data_1 value = 0 }
```

### No Loops
Use Python generators for repetitive patterns.

### Access Syntax
- Script: `value = var:my_variable`
- GUI: `[Player.Var('my_variable')]`

---

## 4. On_Action Hooks

### Extending Base Hooks
```
monthly_country_pulse = {
    on_actions = { my_custom_action }
}

my_custom_action = {
    trigger = { is_ai = no }  # ALWAYS FILTER
    effect = { ... }
}
```

**Performance**: `monthly_country_pulse` fires for EVERY country. Always use `is_ai = no`.

---

## 5. File Encoding

### Localization: UTF-8 BOM Required
```python
open(file, 'w', encoding='utf-8-sig')
```
Or bash: `printf '\xEF\xBB\xBF' > file.yml`

Without BOM = silent failure.

---

## 6. GUI Patterns

### Window Toggle (no scripted_gui)
```
visible = "[GetVariableSystem.Exists('window_open')]"
onclick = "[GetVariableSystem.Set('window_open', 'yes')]"
onclick = "[GetVariableSystem.Clear('window_open')]"
```

### Tabs
```
down = "[GetVariableSystem.Exists('tab_2')]"
visible = "[GetVariableSystem.Exists('tab_2')]"
```

### Grid Lines (manual)
```
widget = {
    position = { 0 50% }
    size = { 100% 1 }
    background = { color = { 1 1 1 0.15 } }
}
```

---

## 7. Code Generation

### When to Use Python
- 60+ similar lines
- Grid patterns (N×M)
- State machines
- Any N > 10 repetitions

### 60-Slot Rotation Pattern
```python
for i in range(59, 0, -1):
    print(f"set_variable = {{ name = data_{i} value = var:data_{i-1} }}")
print(f"set_variable = {{ name = data_0 value = current_value }}")
```

### Output Location
```
mod/scripts/generate.py      # Dev tool
mod/in_game/common/...       # Generated output
```

---

## 8. Debugging

### Error Log
`Documents/Paradox Interactive/Europa Universalis V/logs/error.log`

### Common Errors
| Error | Cause |
|-------|-------|
| `Expected member (tags)` | Missing required metadata.json field |
| `Failed to open file` | Bad path or permissions |
| Variable undefined | Not initialized before use |
| Silent loc failure | Missing UTF-8 BOM |

---

## 9. Quick Reference

### GUI Data Access
| Data | Function |
|------|----------|
| Treasury | `[Player.GetGold]` |
| Tax Base | `[Player.GetTotalTaxBase]` |
| Population | `[Player.GetTotalPopulation]` |
| Custom var | `[Player.Var('name')]` |

### Historical Data (built-in only)
| Function | Returns |
|----------|---------|
| `Player.GetHistoricalTaxBase` | plotpoints |
| `Player.GetHistoricalMaxTaxBase` | number |
| `Player.GetStartDataDate` | date string |

---

## Summary: Key Gotchas

1. **Mods in Documents**, not game folder
2. **metadata.json**: ALL fields required, `id` = empty string
3. **Use `in_game/` wrapper** in mod structure
4. **plotpoints**: Built-in functions only
5. **No loops/dynamic vars**: Use Python generators
6. **Localization needs BOM**
7. **Filter monthly hooks**: `is_ai = no`
8. **WSL symlinks don't work**: Use Windows junctions
