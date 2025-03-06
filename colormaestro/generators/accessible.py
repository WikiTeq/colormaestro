from ..utils import color_conversion
from ..utils import accessibility

def generate(base_color, num_colors):
    """Generate an accessible color palette that meets WCAG contrast guidelines

    Args:
        base_color (tuple): RGB color tuple (0-255, 0-255, 0-255)
        num_colors (int): Number of colors to generate

    Returns:
        list: List of RGB color tuples
    """
    # Convert to HSV for easier manipulation
    h, s, v = color_conversion.rgb_to_hsv(base_color)

    # Start with the base color
    palette = [base_color]

    # Standard text colors
    white = (255, 255, 255)
    black = (0, 0, 0)

    # Check if base color needs adjustment to meet accessibility
    base_with_white = accessibility.calculate_contrast_ratio(base_color, white)
    base_with_black = accessibility.calculate_contrast_ratio(base_color, black)

    # If neither contrast is sufficient, adjust the base color
    if base_with_white < 4.5 and base_with_black < 4.5:
        # Make color more saturated and either darker or lighter
        new_s = min(1.0, s + 0.2)
        new_v = min(0.9, v + 0.3) if base_with_white > base_with_black else max(0.1, v - 0.3)
        adjusted_base = color_conversion.hsv_to_rgb((h, new_s, new_v))

        # Replace base color if adjustment improves contrast
        new_with_white = accessibility.calculate_contrast_ratio(adjusted_base, white)
        new_with_black = accessibility.calculate_contrast_ratio(adjusted_base, black)

        if max(new_with_white, new_with_black) > max(base_with_white, base_with_black):
            palette[0] = adjusted_base
            base_color = adjusted_base

    # Create complementary color with good contrast
    h_comp = (h + 0.5) % 1.0

    # Try different saturation/value combinations to find good contrast
    best_contrast = 0
    best_complement = None

    for s_adj in [0.7, 0.8, 0.9, 1.0]:
        for v_adj in [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
            test_color = color_conversion.hsv_to_rgb((h_comp, s_adj, v_adj))
            contrast = accessibility.calculate_contrast_ratio(base_color, test_color)

            if contrast > best_contrast and contrast >= 4.5:
                best_contrast = contrast
                best_complement = test_color

    # If we found a good complement, add it
    if best_complement:
        palette.append(best_complement)
    else:
        # If no good complement, use a very different value
        new_v = 0.9 if v < 0.5 else 0.1
        palette.append(color_conversion.hsv_to_rgb((h_comp, s, new_v)))

    # Generate remaining colors
    if num_colors > 2:
        # Create a set of hues evenly distributed around the color wheel
        for i in range(2, num_colors):
            step = 1.0 / (num_colors - 1)
            new_h = (h + step * i) % 1.0

            # Try different saturation/value combinations
            best_contrast = 0
            best_color = None

            for s_adj in [0.7, 0.8, 0.9, 1.0]:
                for v_adj in [0.3, 0.5, 0.7, 0.9]:
                    test_color = color_conversion.hsv_to_rgb((new_h, s_adj, v_adj))

                    # Calculate minimum contrast with existing colors
                    min_contrast = min(
                        accessibility.calculate_contrast_ratio(test_color, existing)
                        for existing in palette
                    )

                    if min_contrast > best_contrast and min_contrast >= 3.0:
                        best_contrast = min_contrast
                        best_color = test_color

            # Add the best color or fall back to a default
            if best_color:
                palette.append(best_color)
            else:
                # Fallback: create a color with different lightness
                new_v = 0.8 if i % 2 == 0 else 0.4
                palette.append(color_conversion.hsv_to_rgb((new_h, 0.8, new_v)))

    return palette
