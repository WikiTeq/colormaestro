def rgb_to_hex(rgb):
    """Convert RGB tuple to hex string"""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def generate(palette):
    """Generate CSS variables from the color palette

    Args:
        palette (list): List of RGB color tuples

    Returns:
        str: CSS variables definition
    """
    css = ":root {\n"

    # Add color variables
    for i, color in enumerate(palette):
        hex_color = rgb_to_hex(color)
        var_name = ""

        if i == 0:
            var_name = "--color-primary"
        elif i == 1:
            var_name = "--color-secondary"
        elif i == 2:
            var_name = "--color-accent"
        else:
            var_name = f"--color-{i+1}"

        css += f"  {var_name}: {hex_color};\n"

        # Add RGB components for rgba() usage
        css += f"  {var_name}-rgb: {color[0]}, {color[1]}, {color[2]};\n"

    # Add functional/semantic variables
    css += "\n  /* Semantic color mapping */\n"
    css += "  --color-background: var(--color-primary);\n"
    css += "  --color-text: #000000;\n"
    css += "  --color-button: var(--color-secondary);\n"
    css += "  --color-border: rgba(var(--color-primary-rgb), 0.2);\n"
    css += "  --color-highlight: var(--color-accent);\n"

    css += "}\n"

    # Add dark mode if we have enough colors
    if len(palette) >= 5:
        css += "\n@media (prefers-color-scheme: dark) {\n"
        css += "  :root {\n"
        css += "    --color-text: #ffffff;\n"
        css += "    --color-background: #121212;\n"
        css += "    --color-border: rgba(255, 255, 255, 0.1);\n"
        css += "  }\n"
        css += "}\n"

    return css
