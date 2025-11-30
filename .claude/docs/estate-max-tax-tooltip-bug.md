# Estate Max Tax Tooltip Bug - Investigation & Fixes

## Overview

The `estate_max_tax_tooltip` mod adds a breakdown tooltip showing the sources of estate maximum tax values. Two bugs were identified and partially fixed.

## Bug 1: Localization Key Not Resolving (FIXED)

**Symptom:** `ESTATE_MAX_TAX_LABEL` displayed as raw key instead of "Maximum Tax"

**Root Cause:** Localization file was ASCII encoded. EU5 requires UTF-8 with BOM (Byte Order Mark).

**File:** `game/mod/estate_max_tax_tooltip/in_game/localization/english/estate_max_tax_l_english.yml`

**Fix Applied:**
```python
# Write with UTF-8 BOM encoding
with open(filepath, 'w', encoding='utf-8-sig') as f:
    f.write(content)
```

**Verification:** `hexdump -C <file> | head -1` should show `ef bb bf` at byte positions 0-2.

**Current File Contents:**
```yaml
l_english:
  ESTATE_MAX_TAX_LABEL: "Maximum Tax"
  ESTATE_MAX_TAX_BASE: "Base"
```

## Bug 2: Numbers Don't Add Up (PARTIALLY FIXED - NEEDS CORRECTION)

**Symptom:** Tooltip shows max tax as ~10%, but modifier breakdown only shows ~-16% in penalties with no base value displayed.

**Investigation Results:**

### Where the Base Value Comes From

The TRUE base for estate max tax is **30%**, defined in:

**File:** `game/in_game/common/auto_modifiers/country.txt`
```
country_base_values = {
    ...
    global_estate_max_tax = 0.30
    ...
}
```

### Misleading Modifier: parliament_approved_extra_taxes

**File:** `game/main_menu/common/static_modifiers/country.txt`
```
parliament_approved_extra_taxes = {
    icon = pec_parliament
    global_estate_max_tax = 0.25
}
```

This is NOT the base value. It's a **conditional bonus** (+25%) that only applies when:
1. Country has a parliament
2. Parliament approves extra taxes
3. Effect lasts approximately 1 year

### Estate-Specific Modifiers

Each estate type has its own modifier that adjusts the base:
- `nobles_estate_max_tax`
- `clergy_estate_max_tax`
- `burghers_estate_max_tax`
- `peasants_estate_max_tax`
- `dhimmi_estate_max_tax`
- `tribes_estate_max_tax`
- `cossacks_estate_max_tax`

**Calculation:** `Final Max Tax = Base (30%) + Estate-Specific Modifiers`

Example: 30% base - 16% from privileges = 14% (or ~10% depending on active privileges)

## Current Fix Applied (NEEDS CORRECTION)

Added "Base: 25%" row to the tooltip breakdown for all 7 estate types.

**File:** `game/mod/estate_max_tax_tooltip/in_game/gui/shared/government_tooltips.gui`

**Pattern added after each `TooltipListBase`:**
```
TooltipManualTableField = {
    text_single = {
        text = "ESTATE_MAX_TAX_BASE"
    }
    expand = {}
    text_single = {
        raw_text = "25%"  # ERROR: Should be 30%
    }
}
```

**Estate blocks modified:**
- Nobles (~line 2346)
- Clergy (~line 2430)
- Burghers (~line 2514)
- Peasants (~line 2598)
- Dhimmi (~line 2682)
- Tribes (~line 2766)
- Cossacks (~line 2850)

## PENDING FIX

**Action Required:** Change `raw_text = "25%"` to `raw_text = "30%"` in all 7 estate blocks.

The 25% value was incorrectly taken from `parliament_approved_extra_taxes`, which is a conditional modifier, not the base.

## Key Files Reference

| File | Purpose |
|------|---------|
| `game/mod/estate_max_tax_tooltip/in_game/gui/shared/government_tooltips.gui` | GUI tooltip definitions (needs 25%→30% fix) |
| `game/mod/estate_max_tax_tooltip/in_game/localization/english/estate_max_tax_l_english.yml` | Localization strings (fixed encoding) |
| `game/in_game/common/auto_modifiers/country.txt` | TRUE base value source (30%) |
| `game/main_menu/common/static_modifiers/country.txt` | Conditional parliament modifier (25%) |

## GUI Pattern for Estate Max Tax Breakdown

```
# Header with total value
TooltipListBase = {
    visible = "[And(Not(Estate.GetType.IsAlwaysLoyal), ObjectsEqual(Player.GetGovernment.GetEstateFromKey('ESTATE_KEY').GetType, Estate.GetType))]"
    TooltipManualTableField = {
        text_single = { text = "ESTATE_MAX_TAX_LABEL" }
        expand = {}
        text_single = { raw_text = "[Player.GetModifierValue('ESTATE_TYPE_max_tax')|%0]" }
    }
}

# Base row (add after TooltipListBase)
TooltipManualTableField = {
    text_single = { text = "ESTATE_MAX_TAX_BASE" }
    expand = {}
    text_single = { raw_text = "30%" }  # Corrected value
}

# Modifier breakdown list
TooltipStringPairList = {
    visible = "[same condition as above]"
    datacontext = "[Player.GetModifierTooltipContext('ESTATE_TYPE_max_tax')]"
    textcontext = "[CountryModifierWrap.GetTooltip]"
}
```

Estate keys: `nobles_estate`, `clergy_estate`, `burghers_estate`, `peasants_estate`, `dhimmi_estate`, `tribes_estate`, `cossacks_estate`
