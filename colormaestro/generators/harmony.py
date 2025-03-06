from ..utils import color_conversion

def generate(base_color, harmony_type, num_colors):
    """Generate a color palette based on color harmony principles

    Args:
        base_color (tuple): RGB color tuple (0-255, 0-255, 0-255)
        harmony_type (str): Type of harmony ('complementary', 'analogous', 'triadic', 'tetradic')
        num_colors (int): Number of colors to generate

    Returns:
        list: List of RGB color tuples
    """
    # Convert to HSV for easier manipulation
    h, s, v = color_conversion.rgb_to_hsv(base_color)

    # Start with the base color
    palette = [base_color]

    # Generate harmony colors based on type
    if harmony_type == "complementary":
        # Complementary color (opposite on the color wheel)
        h_comp = (h + 0.5) % 1.0
        comp_color = color_conversion.hsv_to_rgb((h_comp, s, v))
        palette.append(comp_color)

        # Fill remaining colors with variations
        remaining = num_colors - 2
        if remaining > 0:
            # Add variations of the two main colors
            for i in range(remaining):
                if i % 2 == 0:
                    # Variation of base color
                    new_s = max(0.2, min(1.0, s - 0.3 + (0.6 * i / remaining)))
                    new_v = max(0.3, min(1.0, v - 0.2 + (0.4 * i / remaining)))
                    palette.append(color_conversion.hsv_to_rgb((h, new_s, new_v)))
                else:
                    # Variation of complementary color
                    new_s = max(0.2, min(1.0, s - 0.3 + (0.6 * i / remaining)))
                    new_v = max(0.3, min(1.0, v - 0.2 + (0.4 * i / remaining)))
                    palette.append(color_conversion.hsv_to_rgb((h_comp, new_s, new_v)))

    elif harmony_type == "analogous":
        # Analogous colors (adjacent on the color wheel)
        step = 0.08  # About 30 degrees

        # Generate colors on both sides of the base color
        for i in range(1, num_colors):
            if i % 2 == 1:
                # Colors to the right
                h_new = (h + step * ((i + 1) // 2)) % 1.0
            else:
                # Colors to the left
                h_new = (h - step * (i // 2)) % 1.0

            # Slightly vary saturation and value for more interest
            s_new = min(1.0, s * (1.0 + (i % 3 - 1) * 0.1))
            v_new = min(1.0, v * (1.0 + (i % 2 - 0.5) * 0.1))

            palette.append(color_conversion.hsv_to_rgb((h_new, s_new, v_new)))

    elif harmony_type == "triadic":
        # Triadic colors (evenly spaced around the color wheel)
        h1 = (h + 1/3) % 1.0
        h2 = (h + 2/3) % 1.0

        palette.append(color_conversion.hsv_to_rgb((h1, s, v)))
        palette.append(color_conversion.hsv_to_rgb((h2, s, v)))

        # Fill remaining colors
        remaining = num_colors - 3
        if remaining > 0:
            for i in range(remaining):
                h_base = [h, h1, h2][i % 3]
                new_s = max(0.2, min(1.0, s - 0.2 + (0.4 * i / remaining)))
                new_v = max(0.3, min(1.0, v - 0.1 + (0.2 * i / remaining)))
                palette.append(color_conversion.hsv_to_rgb((h_base, new_s, new_v)))

    elif harmony_type == "tetradic":
        # Tetradic/rectangular (two complementary pairs)
        h1 = (h + 0.25) % 1.0
        h2 = (h + 0.5) % 1.0
        h3 = (h + 0.75) % 1.0

        palette.append(color_conversion.hsv_to_rgb((h1, s, v)))
        palette.append(color_conversion.hsv_to_rgb((h2, s, v)))
        palette.append(color_conversion.hsv_to_rgb((h3, s, v)))

        # Fill remaining colors
        remaining = num_colors - 4
        if remaining > 0:
            for i in range(remaining):
                h_base = [h, h1, h2, h3][i % 4]
                new_s = max(0.2, min(1.0, s - 0.2 + (0.4 * i / remaining)))
                new_v = max(0.3, min(1.0, v - 0.1 + (0.2 * i / remaining)))
                palette.append(color_conversion.hsv_to_rgb((h_base, new_s, new_v)))

    return palette
