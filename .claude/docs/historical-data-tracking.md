# EU5 Historical Data Tracking System

Research findings on how to capture and store historical data for graphing in EU5 mods.

## On_Action Hooks for Periodic Capture

### Available Pulse Events

| Hook | Frequency | Location |
|------|-----------|----------|
| `monthly_country_pulse` | Every month | `common/on_action/country_monthly.txt` |
| `yearly_country_pulse` | Every year | `common/on_action/country_yearly.txt` |
| `country_biyearly` | Every 2 years | `common/on_action/country_biyearly.txt` |
| `country_four_yearly` | Every 4 years | `common/on_action/country_four_yearly.txt` |

### Hooking Into Monthly Pulse

```
# common/on_action/my_monthly_hook.txt
monthly_country_pulse = {
    on_actions = {
        my_custom_monthly_action
    }
}

my_custom_monthly_action = {
    trigger = {
        is_ai = no  # Only for human player
    }
    effect = {
        my_capture_effect = yes
    }
}
```

## Variable Storage System

### Scalar Variables

```
set_variable = {
    name = my_variable
    value = 100
}

# With expiration
set_variable = {
    name = temp_flag
    value = yes
    years = 5        # Auto-removes after 5 years
    months = 18      # Or use months
}
```

### List Variables

```
# Add to list
add_to_variable_list = {
    name = my_data_list
    target = 42.5
}

# Check list size (trigger)
list_size = { name = my_list value > 0 }

# Iterate all items
every_in_list = {
    list = my_list
    # effects here
}

# Clear list
clear_global_variable_list = my_list
```

## Historical Data Storage Pattern

### 60-Slot Rotation (Recommended)

For tracking 60 months (5 years) of history with direct access:

```
capture_monthly_data = {
    # Rotate: shift all slots forward
    set_variable = { name = data_h_59 value = var:data_h_58 }
    set_variable = { name = data_h_58 value = var:data_h_57 }
    # ... (repeat for all 59 slots)
    set_variable = { name = data_h_1 value = var:data_h_0 }

    # Store current value in slot 0
    set_variable = { name = data_h_0 value = gold }
}
```

**Pros:**
- O(1) direct access to any slot (needed for tooltips)
- Compatible with GUI plotpoints binding
- Persists correctly across save/load

**Cons:**
- Requires boilerplate (use Python code generator)
- Fixed size (60 slots = 360 variables for 6 metrics)

### List-Based Alternative

```
add_to_variable_list = {
    name = gold_history
    target = gold
}

# Trim to keep only last 60
if = {
    limit = { list_size = { name = gold_history value > 60 } }
    # Would need to rebuild list (complex)
}
```

**Pros:** Simpler code, unbounded size
**Cons:** O(n) iteration, no direct index access

## Plotpoints Data Format

### Built-in Historical Functions

```
Player.GetHistoricalPopulation      # Returns plotpoints array
Country.GetHistoricalTaxBase        # Returns plotpoints array
Player.GetHistoricalMaxPopulation   # Peak value
Player.GetHistoricalMinPopulation   # Lowest value
```

### GUI Usage

```
plotline = {
    size = { 100% 100% }
    using = plot_line
    width = 3

    plotpoints = "[Country.GetHistoricalTaxBase]"
}

# With axis labels
axis = {
    direction = vertical  # or horizontal
    axis_label = {
        text_single = {
            raw_text = "[Country.GetHistoricalMaxTaxBase|2]"
        }
    }
}
```

### Custom Data to Plotpoints

For custom tracked data, options:
1. **String concatenation** (if supported): Build plot string from variables
2. **Individual elements**: 60 GUI widgets positioned by X coordinate
3. **Scripted GUI iteration**: Dynamic visualization builder

## Statistics Calculation

```
calculate_statistics = {
    # Average
    set_variable = {
        name = gold_avg_60m
        value = {
            value = 0
            add = var:gold_h_0
            add = var:gold_h_1
            # ... all 60
            divide = 60
        }
    }

    # Change over period
    set_variable = {
        name = gold_change_60m
        value = {
            value = var:gold_h_0
            subtract = var:gold_h_59
        }
    }
}
```

## Limitations

| Limitation | Workaround |
|------------|------------|
| No dynamic loop counts | Hardcode bounds, use code generators |
| No array indexing `list[5]` | Use named slots or iteration |
| Variable names are static | Can't do `var:data_$i$` |
| Lists don't support removal by index | Rebuild entire list |
| No built-in averaging | Manual sum and divide |

## Performance Considerations

- `monthly_country_pulse` fires every month - keep effects lightweight
- List iteration scales linearly with size
- 360 variables (6 metrics × 60 slots) is acceptable
- Only track for human player (`is_ai = no`)
