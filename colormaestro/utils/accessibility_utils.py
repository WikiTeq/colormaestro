def calculate_contrast_ratio(color1, color2):
    """Calculate the contrast ratio between two colors according to WCAG 2.0

    Args:
        color1 (tuple): RGB color tuple (0-255, 0-255, 0-255)
        color2 (tuple): RGB color tuple (0-255, 0-255, 0-255)

    Returns:
        float: Contrast ratio (1 to 21)
    """
    # Calculate relative luminance for each color
    l1 = calculate_relative_luminance(color1)
    l2 = calculate_relative_luminance(color2)

    # Calculate contrast ratio
    if l1 > l2:
        return (l1 + 0.05) / (l2 + 0.05)
    else:
        return (l2 + 0.05) / (l1 + 0.05)

def calculate_relative_luminance(rgb):
    """Calculate the relative luminance of a color according to WCAG 2.0

    Args:
        rgb (tuple): RGB color tuple (0-255, 0-255, 0-255)

    Returns:
        float: Relative luminance (0 to 1)
    """
    # Normalize RGB values to 0-1 range
    r, g, b = rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0

    # Convert to sRGB
    r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4

    # Calculate luminance
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def check_contrast(palette):
    """Check contrast between all color pairs in a palette

    Args:
        palette (list): List of RGB color tuples

    Returns:
        list: List of dictionaries with contrast information for each pair
    """
    results = []

    # Check all unique pairs
    for i, color1 in enumerate(palette):
        for j, color2 in enumerate(palette):
            if i < j:  # Only check each pair once
                ratio = calculate_contrast_ratio(color1, color2)
                passes_aa = ratio >= 4.5  # AA standard for normal text
                passes_aaa = ratio >= 7.0  # AAA standard for normal text

                results.append({
                    'color1': color1,
                    'color2': color2,
                    'ratio': round(ratio, 2),
                    'passes_aa': passes_aa,
                    'passes_aaa': passes_aaa
                })

    return results

def display_results(results):
    """Display contrast check results in a readable format

    Args:
        results (list): List of contrast result dictionaries
    """
    print("Contrast Ratio Analysis:")
    print("───────────────────────")

    for result in results:
        c1 = result['color1']
        c2 = result['color2']
        ratio = result['ratio']
        passes_aa = result['passes_aa']
        passes_aaa = result['passes_aaa']

        # Create status indicator
        status = "✓✓" if passes_aaa else "✓" if passes_aa else "✗"

        print(f"Colors: RGB{c1} vs RGB{c2}")
        print(f"Ratio: {ratio}:1  Status: {status}")
        if not passes_aa:
            print("⚠️ Does not pass WCAG AA standard (4.5:1)")
        elif not passes_aaa:
            print("ℹ️ Passes AA but not AAA standard (7:1)")
        print("───────────────────────")
