#!/usr/bin/env python3
"""
Generate dot-based visualization widgets for custom historical data.

Instead of plotlines (which require opaque plotpoints format), this creates
60 small dot widgets positioned across the graph area, each reading from
one slot variable.

The Y position is calculated as a percentage based on min/max values.
"""

SLOTS = 60
METRIC = "gold"  # Change for different metrics

def generate_dots_gui(metric: str) -> str:
    """Generate 60 dot widgets for one metric."""
    lines = []

    lines.append(f"# Auto-generated dot visualization for {metric}")
    lines.append(f"# Each dot reads from {metric}_h_N and positions based on min/max")
    lines.append("")
    lines.append("widget = {")
    lines.append("    size = { 100% 100% }")
    lines.append("")

    for i in range(SLOTS):
        # X position: slot 0 = rightmost (current), slot 59 = leftmost (oldest)
        # So we invert: slot 0 -> 100%, slot 59 -> 0%
        x_percent = 100 - (i * 100 / (SLOTS - 1))

        lines.append(f"    # Slot {i}")
        lines.append(f"    widget = {{")
        lines.append(f"        size = {{ 6 6 }}")
        lines.append(f"        position = {{ {x_percent:.1f}% 0 }}")
        lines.append(f"        parentanchor = left")
        lines.append(f"        ")
        lines.append(f"        # Y position calculated from variable value")
        lines.append(f"        # This requires a way to compute percentage from value...")
        lines.append(f"        # position_y = \"[Subtract(100, Multiply(Divide(Player.Var('{metric}_h_{i}'), Player.Var('{metric}_max_60m')), 100))]%\"")
        lines.append(f"        ")
        lines.append(f"        background = {{")
        lines.append(f"            color = {{ 0.9 0.75 0.2 1.0 }}")
        lines.append(f"        }}")
        lines.append(f"        ")
        lines.append(f"        tooltip = \"[Player.Var('{metric}_h_{i}')|2] ({SLOTS - i} months ago)\"")
        lines.append(f"    }}")
        lines.append("")

    lines.append("}")

    return "\n".join(lines)


def generate_simplified_approach() -> str:
    """
    Alternative: Use visibility conditions instead of dynamic positioning.

    Create 10 'bands' at different Y positions (0%, 10%, 20%... 90%)
    Each slot has 10 widgets, only one visible based on value range.
    """
    lines = []
    lines.append("# Simplified band-based visualization")
    lines.append("# Uses visibility conditions instead of dynamic positioning")
    lines.append("")
    lines.append("# For each slot, show a dot at one of 10 Y positions")
    lines.append("# based on which 'band' the value falls into")
    lines.append("")

    for slot in range(SLOTS):
        x_percent = 100 - (slot * 100 / (SLOTS - 1))

        lines.append(f"# Slot {slot} - X position {x_percent:.1f}%")

        # Create 10 bands (0-10%, 10-20%, etc. of max value)
        for band in range(10):
            y_percent = 90 - (band * 10)  # Band 0 = bottom, Band 9 = top

            lines.append(f"widget = {{")
            lines.append(f"    size = {{ 4 4 }}")
            lines.append(f"    position = {{ {x_percent:.1f}% {y_percent}% }}")
            lines.append(f"    parentanchor = left|vcenter")
            lines.append(f"    ")
            lines.append(f"    # Visible when value is in band {band} ({band*10}%-{(band+1)*10}% of max)")
            lines.append(f"    visible = \"[And(")
            lines.append(f"        GreaterThanOrEqualTo_CFixedPoint(")
            lines.append(f"            Player.Var('gold_h_{slot}'),")
            lines.append(f"            Multiply_CFixedPoint(Player.Var('gold_max_60m'), '(CFixedPoint){band/10:.1f}')")
            lines.append(f"        ),")
            lines.append(f"        LessThan_CFixedPoint(")
            lines.append(f"            Player.Var('gold_h_{slot}'),")
            lines.append(f"            Multiply_CFixedPoint(Player.Var('gold_max_60m'), '(CFixedPoint){(band+1)/10:.1f}')")
            lines.append(f"        )")
            lines.append(f"    )]\"")
            lines.append(f"    ")
            lines.append(f"    background = {{ color = {{ 0.9 0.75 0.2 1.0 }} }}")
            lines.append(f"}}")
            lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    # Generate the concept (not directly usable due to dynamic positioning limitations)
    print("=== DOT VISUALIZATION CONCEPT ===")
    print("The challenge: GUI cannot dynamically position based on variable values.")
    print("")
    print("=== SOLUTION: BAND-BASED VISIBILITY ===")
    print("Instead of dynamic Y positioning, use 10 Y bands with visibility conditions.")
    print("This creates 600 widgets (60 slots × 10 bands) but only 60 are visible at once.")
    print("")
    print("Trade-off: Less precise (10% resolution) but actually works in Paradox GUI.")
    print("")

    # Write a small example
    example = """
# Example for ONE slot (slot 0 = current month)
# Shows a dot at one of 10 Y positions based on gold value

# Band 0 (0-10% of max) - bottom
widget = {
    size = { 4 4 }
    position = { 100% 90% }
    visible = "[And(
        GreaterThanOrEqualTo_CFixedPoint(Player.Var('gold_h_0'), '(CFixedPoint)0'),
        LessThan_CFixedPoint(Player.Var('gold_h_0'), Multiply_CFixedPoint(Player.Var('gold_max_60m'), '(CFixedPoint)0.1'))
    )]"
    background = { color = { 0.9 0.75 0.2 1.0 } }
    tooltip = "Treasury: [Player.Var('gold_h_0')|2]"
}

# Band 5 (50-60% of max) - middle
widget = {
    size = { 4 4 }
    position = { 100% 40% }
    visible = "[And(
        GreaterThanOrEqualTo_CFixedPoint(Player.Var('gold_h_0'), Multiply_CFixedPoint(Player.Var('gold_max_60m'), '(CFixedPoint)0.5')),
        LessThan_CFixedPoint(Player.Var('gold_h_0'), Multiply_CFixedPoint(Player.Var('gold_max_60m'), '(CFixedPoint)0.6'))
    )]"
    background = { color = { 0.9 0.75 0.2 1.0 } }
    tooltip = "Treasury: [Player.Var('gold_h_0')|2]"
}

# ... (8 more bands for this slot, then repeat for slots 1-59)
"""
    print(example)

    with open("dot_visualization_concept.txt", "w") as f:
        f.write("# DOT-BASED VISUALIZATION CONCEPT\n")
        f.write("# \n")
        f.write("# This approach uses visibility conditions instead of dynamic positioning.\n")
        f.write("# Creates 600 widgets (60 slots × 10 Y bands), but only 60 visible at once.\n")
        f.write("# \n")
        f.write("# Resolution: 10% bands (not as smooth as plotline, but functional)\n")
        f.write("# Includes tooltips showing exact values on hover!\n")
        f.write("#\n\n")
        f.write(example)

    print("Written concept to dot_visualization_concept.txt")
