from ..utils import color_conversion

def rgb_to_hex(rgb):
    """Convert RGB tuple to hex string"""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def generate(palette):
    """Generate a Tailwind CSS config for the color palette

    Args:
        palette (list): List of RGB color tuples

    Returns:
        str: Tailwind CSS config section for colors
    """
    config = "// tailwind.config.js\n"
    config += "module.exports = {\n"
    config += "  theme: {\n"
    config += "    extend: {\n"
    config += "      colors: {\n"

    # Add primary color with shades
    primary = palette[0]
    primary_hex = rgb_to_hex(primary)
    primary_h, primary_s, primary_l = color_conversion.rgb_to_hsl(primary)

    config += "        primary: {\n"
    config += f"          DEFAULT: '{primary_hex}',\n"

    # Generate primary color shades (50, 100, 200, ..., 900)
    for i, shade in enumerate([50, 100, 200, 300, 400, 500, 600, 700, 800, 900]):
        # Adjust lightness for each shade
        # 50 is lightest (high lightness), 900 is darkest (low lightness)
        l_adjusted = 0.95 - (i * 0.08)  # 0.95 to 0.23

        # Keep within bounds
        l_adjusted = max(0.05, min(0.95, l_adjusted))

        # Adjust saturation slightly for more natural color scale
        s_adjusted = primary_s
        if l_adjusted > 0.8:  # Lighter colors are less saturated
            s_adjusted = max(0.05, primary_s * 0.7)
        elif l_adjusted < 0.3:  # Darker colors slightly more saturated
            s_adjusted = min(1.0, primary_s * 1.2)

        shade_color = color_conversion.hsl_to_rgb((primary_h, s_adjusted, l_adjusted))
        shade_hex = rgb_to_hex(shade_color)

        config += f"          '{shade}': '{shade_hex}',\n"

    config += "        },\n"

    # Add secondary color if available
    if len(palette) > 1:
        secondary = palette[1]
        secondary_hex = rgb_to_hex(secondary)
        config += f"        secondary: '{secondary_hex}',\n"

    # Add accent color if available
    if len(palette) > 2:
        accent = palette[2]
        accent_hex = rgb_to_hex(accent)
        config += f"        accent: '{accent_hex}',\n"

    # Add remaining colors
    for i in range(3, len(palette)):
        color = palette[i]
        hex_value = rgb_to_hex(color)
        config += f"        'color-{i+1}': '{hex_value}',\n"

    config += "      },\n"
    config += "    },\n"
    config += "  },\n"
    config += "  variants: {},\n"
    config += "  plugins: [],\n"
    config += "};\n"

    return config
