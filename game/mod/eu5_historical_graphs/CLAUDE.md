# EU5 Historical Graphs Mod

Enhanced historical visualization: multi-line graphs, tooltips, grid lines, 5-year tracking.

## Architecture

**Hybrid approach** (due to plotline limitations):
1. Built-in plotlines for smooth graphs (`GetHistoricalTaxBase`, `GetHistoricalPopulation`)
2. Custom 60-slot variable rotation for data capture
3. Dot overlays at yearly intervals for hover tooltips

## Structure

```
eu5_historical_graphs/
├── .metadata/metadata.json
├── in_game/
│   ├── common/
│   │   ├── on_action/graphs_monthly_pulse.txt
│   │   └── scripted_effects/
│   │       ├── graphs_capture_effects.txt    # Generated
│   │       ├── graphs_statistics_effects.txt # Generated
│   │       └── graphs_utility_effects.txt
│   ├── gui/graphs_main_window.gui
│   └── localization/english/graphs_l_english.yml
└── scripts/generate_capture_effects.py
```

## Key Systems

### Monthly Capture
Hook: `monthly_country_pulse` → `graphs_historical_data_capture`
- Filter: `is_ai = no` (performance critical)
- Captures: gold, taxbase, population, manpower, income, stability

### 60-Slot Rotation
Each metric has 60 variables (`gold_h_0` to `gold_h_59`).
Monthly: shift all down, store current in slot 0.

### Tooltip Markers
5 dots at X positions 100%, 80%, 60%, 40%, 20% (years 0-4).
Reference variables: `gold_h_0`, `gold_h_12`, `gold_h_24`, `gold_h_36`, `gold_h_48`.

## Regenerating Effects

```bash
cd scripts && python generate_capture_effects.py
# Output goes to in_game/common/scripted_effects/
```

## Development

Junction from Documents to game/mod (see root CLAUDE.md).
Edit here, game loads from Documents via junction.

## See Also

- `/.claude/docs/engineering-lessons.md` - Critical limitations
- `/CLAUDE.md` - EU5 modding reference
