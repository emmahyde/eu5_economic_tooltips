# Better Tooltips Mod

A UI enhancement mod for Europa Universalis V that improves tooltip information display and adds useful data to the topbar and economy panels.

## Features

### 1. Enhanced Topbar Estate Display

**File:** `in_game/gui/hud_topbar.gui`

Completely redesigned the estate section in the topbar to show more useful information at a glance:

**Changes from vanilla:**
- **2-row condensed layout** per estate instead of the original progress bar design
- **Row 1:** Estate icon + Power%/Satisfaction% (e.g., `42%/75%`)
- **Row 2:** Taxed income from that estate (e.g., `+12.34`)
- Uses `EconomyView.GetTaxRateSettings` datamodel instead of `InGameTopbar.GetEstates` to access income data
- Added `TaxRateSetting.ShouldShow` visibility check to only show estates the player actually has
- Hovering on income value shows the full Estate Income Breakdown tooltip
- Warning icon displayed when taxes cannot be collected from an estate

### 2. Estate Tooltip Improvements

**Files:** `in_game/gui/shared/government_tooltips.gui`, `main_menu/gui/shared/estate_tooltips.gui`

Enhanced the estate tooltip with additional tax information:

**Changes from vanilla:**
- Added "Tax Details" section (renamed from "Maximum Tax")
- "Total" renamed to "Maximum Tax" for clarity
- Added "Taxed Income" line showing current tax revenue from the estate
- Taxed Income line has its own tooltip showing the income breakdown
- Shows warning icon if taxes cannot be collected

### 3. Estate Satisfaction Tooltip Reorder

**File:** `main_menu/gui/shared/estate_tooltips.gui`

Reorganized the estate satisfaction tooltip for better readability:

**Changes from vanilla:**
- **Current satisfaction** now shown first (highlighted)
- **Satisfaction Equilibrium** shown second
- **Monthly Change** shown third
- More logical flow: "Where am I?" → "Where am I going?" → "How fast?"

### 4. Economy Panel Estate Display

**File:** `in_game/gui/economy_lateralview.gui`

Improved the estate tax slider section in the Economy > Balance panel:

**Changes from vanilla:**
- Shows current satisfaction % → target satisfaction % with arrow separator (e.g., `75% > 80%`)
- Face icons (sad/neutral/happy) now based on **current satisfaction** instead of equilibrium
- Proper tooltip on hover showing estate satisfaction details

### 5. RGO Promotion Tooltip with Province Control

**File:** `in_game/gui/shared/location_tooltips.gui`

Enhanced the RGO promotion tooltip to include province control information:

**Additions:**
- **Province Control section** with pie chart visualization
  - Shows current control percentage
  - Shows monthly control change
- **Control Effects section** showing economic impact of control level
- Helps players understand how province control affects RGO output

## Localization

**Files:** `in_game/localization/english/better_tooltips_l_english.yml`, `main_menu/localization/english/better_tooltips_l_english.yml`

New localization keys added:
- `ESTATE_MAX_TAX_LABEL`: "Tax Details"
- `ESTATE_MAX_TAX_TOTAL`: "Maximum Tax"
- `ESTATE_TAXED_INCOME`: "Taxed Income"
- `BETTER_TOOLTIPS_CURRENT`: "Current"
- `BETTER_TOOLTIPS_MONTHLY_CHANGE`: "Monthly Change"
- `BETTER_TOOLTIPS_PROVINCE_CONTROL`: "Province Control"
- `BETTER_TOOLTIPS_CONTROL_EFFECTS`: "Control Effects"

## Technical Notes

- The topbar estate display required switching from `InGameTopbar.GetEstates` (which provides `EstatesItem`) to `EconomyView.GetTaxRateSettings` (which provides `TaxRateSetting`) to access the `GetIncome` function
- `GetEconomyView` datacontext must be set before using `EconomyView.GetTaxRateSettings`
- The `block "extra_tax_details"` in government_tooltips.gui allows the topbar to inject taxed income into the estate tooltip via blockoverride

## Compatibility

- Built for EU5 version 1.0.x
- Overrides vanilla GUI files - may conflict with other mods that modify the same files

## File Structure

```
better_tooltips/
├── .metadata/
│   └── metadata.json
├── in_game/
│   ├── gui/
│   │   ├── economy_lateralview.gui
│   │   ├── hud_topbar.gui
│   │   └── shared/
│   │       ├── government_tooltips.gui
│   │       └── location_tooltips.gui
│   └── localization/
│       └── english/
│           └── better_tooltips_l_english.yml
└── main_menu/
    ├── gui/
    │   └── shared/
    │       └── estate_tooltips.gui
    └── localization/
        └── english/
            └── better_tooltips_l_english.yml
```
