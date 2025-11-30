# EU5 GUI Graph System

Research findings on plotlines, axes, and graph visualization in EU5.

## Core Components

### Plotline Widget

```
plotline = {
    size = { 100% 100% }
    using = plot_line          # Template from plotlines.gui
    width = 3                  # Line thickness
    color = { 0.2 0.8 0.2 1.0 } # RGBA

    plotpoints = "[DataSource.GetPlotPoints]"
    plotrect = "[DataSource.GetPlotRect]"  # Optional scaling

    tooltip = "[DataSource.GetTooltip]"
}
```

### Plot Line Template (from plotlines.gui)

```
template plot_line {
    gfxtype = linegfx
    line_type = line
    line_cap = yes
    alpha = 0.8
    texture = "gfx/lines/white.dds"
}
```

## Axis Labels

### Vertical Axis (Y)

```
axis = {
    size = { 100% 100% }
    direction = vertical

    # Min value (bottom)
    axis_label = {
        text_single = {
            widgetanchor = bottom|left
            parentanchor = left
            raw_text = "[DataSource.GetMinValue]"
        }
    }

    # Max value (top)
    axis_label = {
        text_single = {
            widgetanchor = top|left
            parentanchor = left
            raw_text = "[DataSource.GetMaxValue]"
        }
    }
}
```

### Horizontal Axis (X)

```
axis = {
    size = { 100% 100% }
    direction = horizontal

    # Start (left)
    axis_label = {
        text_single = {
            parentanchor = bottom|left
            raw_text = "Start Date"
        }
    }

    # End (right)
    axis_label = {
        text_single = {
            parentanchor = bottom|right
            raw_text = "End Date"
        }
    }
}
```

## Multiple Lines

### Using extra_plotlines Block

```
caesar_plotline = {
    blockoverride "line_plotpoints" {
        plotpoints = "[DataSource.GetPrimaryData]"
    }
    blockoverride "line_color" {
        color = { 0.2 0.8 0.2 1.0 }  # Green
    }

    blockoverride "extra_plotlines" {
        # Second line
        plotline = {
            size = { 100% 100% }
            using = plot_line
            width = 2
            color = { 0.8 0.2 0.2 0.8 }  # Red
            plotpoints = "[DataSource.GetSecondaryData]"
        }

        # Third line
        plotline = {
            size = { 100% 100% }
            using = plot_line
            width = 2
            color = { 0.2 0.2 0.8 0.8 }  # Blue
            plotpoints = "[DataSource.GetTertiaryData]"
        }
    }
}
```

### Stacking Plotlines (Alternative)

```
widget = {
    size = { 100% 100% }

    plotline = {
        size = { 100% 100% }
        color = { 0.2 0.8 0.2 1.0 }
        plotpoints = "[DataA]"
    }

    plotline = {
        size = { 100% 100% }
        color = { 0.8 0.2 0.2 1.0 }
        plotpoints = "[DataB]"
    }
}
```

## Grid Lines (Manual Implementation)

No built-in grid lines. Create manually:

```
# Horizontal grid lines at fixed percentages
widget = {
    position = { 0 20% }
    size = { 100% 1 }
    background = {
        texture = "gfx/interface/colors/white.dds"
        alpha = 0.2
    }
}
widget = {
    position = { 0 40% }
    size = { 100% 1 }
    background = { texture = "..." alpha = 0.2 }
}
widget = {
    position = { 0 60% }
    size = { 100% 1 }
    background = { texture = "..." alpha = 0.2 }
}
widget = {
    position = { 0 80% }
    size = { 100% 1 }
    background = { texture = "..." alpha = 0.2 }
}
```

## Legend (Manual Implementation)

```
hbox = {
    position = { 10 10 }
    spacing = 15

    # Entry 1
    hbox = {
        spacing = 5
        widget = {
            size = { 20 3 }
            background = {
                texture = "gfx/interface/colors/green.dds"
            }
        }
        text_single = {
            raw_text = "Treasury"
            using = Font_Size_Small
        }
    }

    # Entry 2
    hbox = {
        spacing = 5
        widget = {
            size = { 20 3 }
            background = {
                texture = "gfx/interface/colors/red.dds"
            }
        }
        text_single = {
            raw_text = "Tax Base"
            using = Font_Size_Small
        }
    }
}
```

## Built-in Plotline Types

### caesar_plotline (from plotlines.gui)

Full-featured graph with:
- Header text
- Graph area with plotline
- Y-axis min/max labels
- X-axis start/end date labels
- Background styling

```
caesar_plotline = {
    size = { 400 300 }

    blockoverride "header" { text = "My Graph Title" }
    blockoverride "line_color" { color = { 0.9 0.9 0.9 1.0 } }
    blockoverride "line_plotpoints" { plotpoints = "[Data]" }
    blockoverride "maxvalue" { raw_text = "[MaxVal]" }
    blockoverride "minvalue" { raw_text = "[MinVal]" }
    blockoverride "startdate" { text = "[StartDate]" }
    blockoverride "enddate" { text = "[EndDate]" }
    blockoverride "extra_plotlines" { }
}
```

### economy_plotline

Similar to caesar_plotline but styled for economy panel.

## Hover Tooltips

Add tooltip to plotline:

```
plotline = {
    tooltip = "[SomeObject.GetGraphTooltip]"

    # Or custom tooltip widget
    tooltipwidget = {
        ContextualTooltipType = {
            blockoverride "title_text" { text = "Value" }
            blockoverride "tooltip_content" {
                text_single = { raw_text = "[Value]" }
            }
        }
    }
}
```

## Key GUI Files Reference

| File | Contents |
|------|----------|
| `gui/shared/plotlines.gui` | plot_line template, caesar_plotline, economy_plotline |
| `gui/shared/standard_types.gui` | Basic types, piechart |
| `gui/economy_lateralview.gui` | Economy graph implementation |
| `gui/shared/country_tooltips.gui` | TaxBaseTooltip with graph |
| `gui/ai_currency_viewer.gui` | Advanced graph with X/Y axis example |

## Dynamic Scaling

Use `plotrect` for custom scaling:

```
plotline = {
    plotrect = "[DataSource.GetPlotRect]"  # { minX maxX minY maxY }
    plotpoints = "[DataSource.GetPoints]"
}
```
