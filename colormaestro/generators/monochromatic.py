from ..utils import color_conversion

def generate(base_color, num_colors):
    """Generate a monochromatic color palette from a base color

    Args:
        base_color (tuple): RGB color tuple (0-255, 0-255, 0-255)
        num_colors (int): Number of colors to generate

    Returns:
        list: List of RGB color tuples
    """
    # Convert to HSV for easier manipulation
    h, s, v = color_conversion.rgb_to_hsv(base_color)

    palette = []

    # Create variations by adjusting saturation and value
    for i in range(num_colors):
        # Calculate saturation and value based on position
        if num_colors > 1:
            # For even positions, vary saturation while keeping value high
            if i % 2 == 0:
                new_s = max(0.1, min(1.0, s - 0.3 + (0.6 * i / (num_colors - 1))))
                new_v = v
            # For odd positions, vary value while keeping original saturation
            else:
                new_s = s
                new_v = max(0.3, min(1.0, v - 0.3 + (0.6 * i / (num_colors - 1))))
        else:
            new_s = s
            new_v = v

        # Convert back to RGB and add to palette
        rgb = color_conversion.hsv_to_rgb((h, new_s, new_v))
        palette.append(rgb)

    # Sort by brightness (value)
    palette.sort(key=lambda rgb: sum(rgb), reverse=True)

    return palette
