from ..utils import color_conversion

def generate(base_color, num_colors, dark_mode=False):
    """Generate a complete UI palette from a base color

    Args:
        base_color (tuple): RGB color tuple (0-255, 0-255, 0-255)
        num_colors (int): Number of colors to generate
        dark_mode (bool): Whether to optimize for dark mode

    Returns:
        list: List of RGB color tuples
    """
    # Convert to HSV for easier manipulation
    h, s, v = color_conversion.rgb_to_hsv(base_color)

    # Start with the base color as primary
    primary = base_color

    # Generate secondary color (complementary with adjustments)
    h_secondary = (h + 0.5) % 1.0  # Opposite hue
    s_secondary = max(0.15, s - 0.1)  # Slightly less saturated
    v_secondary = min(0.95, v + 0.05) if v < 0.8 else max(0.8, v - 0.05)
    secondary = color_conversion.hsv_to_rgb((h_secondary, s_secondary, v_secondary))

    # Generate accent color (triadic relationship)
    h_accent = (h + 0.33) % 1.0  # 120° around the color wheel
    s_accent = min(1.0, s + 0.1)  # More saturated
    v_accent = min(1.0, v + 0.05)  # Slightly brighter
    accent = color_conversion.hsv_to_rgb((h_accent, s_accent, v_accent))

    # Create the initial palette with primary, secondary, and accent
    palette = [primary, secondary, accent]

    # Generate neutral colors based on the primary color
    neutral_base_h = h
    neutral_base_s = min(0.08, s * 0.2)  # Very low saturation

    # Generate darker and lighter variants
    if dark_mode:
        # For dark mode, generate more light neutral colors
        for i in range(num_colors - 3):
            neutral_v = 0.3 + (i * 0.6 / (num_colors - 3))  # 0.3 to 0.9
            neutral = color_conversion.hsv_to_rgb((neutral_base_h, neutral_base_s, neutral_v))
            palette.append(neutral)
    else:
        # For light mode, generate more dark neutral colors
        for i in range(num_colors - 3):
            neutral_v = 0.9 - (i * 0.6 / (num_colors - 3))  # 0.9 to 0.3
            neutral = color_conversion.hsv_to_rgb((neutral_base_h, neutral_base_s, neutral_v))
            palette.append(neutral)

    return palette
