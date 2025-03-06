def calculate_contrast_ratio(color1, color2):
    """Calculate WCAG contrast ratio between two colors.

    Args:
        color1 (tuple): RGB color tuple (0-255, 0-255, 0-255)
        color2 (tuple): RGB color tuple (0-255, 0-255, 0-255)

    Returns:
        float: Contrast ratio (1:1 to 21:1)
    """
    # Calculate relative luminance for each color
    def get_luminance(rgb):
        # Convert RGB to sRGB
        srgb = [x / 255.0 for x in rgb]

        # Apply transformations
        for i in range(3):
            if srgb[i] <= 0.03928:
                srgb[i] = srgb[i] / 12.92
            else:
                srgb[i] = ((srgb[i] + 0.055) / 1.055) ** 2.4

        # Calculate luminance
        return 0.2126 * srgb[0] + 0.7152 * srgb[1] + 0.0722 * srgb[2]

    # Get luminance values
    l1 = get_luminance(color1)
    l2 = get_luminance(color2)

    # Calculate contrast ratio
    if l1 > l2:
        return (l1 + 0.05) / (l2 + 0.05)
    else:
        return (l2 + 0.05) / (l1 + 0.05)

def check_contrast(palette):
    """Check contrast ratios between colors in the palette

    Args:
        palette (list): List of RGB color tuples

    Returns:
        dict: Dictionary with contrast check results
    """
    results = {}

    # Check contrast with white and black (for text)
    white = (255, 255, 255)
    black = (0, 0, 0)

    for i, color in enumerate(palette):
        color_name = f"Color {i+1}"
        if i == 0:
            color_name = "Primary"
        elif i == 1:
            color_name = "Secondary"
        elif i == 2:
            color_name = "Accent"

        # Check with white
        white_ratio = calculate_contrast_ratio(color, white)
        white_aa = white_ratio >= 4.5
        white_aaa = white_ratio >= 7.0

        # Check with black
        black_ratio = calculate_contrast_ratio(color, black)
        black_aa = black_ratio >= 4.5
        black_aaa = black_ratio >= 7.0

        results[color_name] = {
            "white_text": {
                "ratio": round(white_ratio, 2),
                "AA": white_aa,
                "AAA": white_aaa
            },
            "black_text": {
                "ratio": round(black_ratio, 2),
                "AA": black_aa,
                "AAA": black_aaa
            }
        }

    return results

def display_results(results):
    """Display accessibility check results in the terminal

    Args:
        results (dict): Dictionary with contrast check results
    """
    import click

    click.echo("\nAccessibility Check Results:\n")

    for color_name, checks in results.items():
        click.echo(f"{color_name}:")

        # White text check
        white_ratio = checks["white_text"]["ratio"]
        white_aa = checks["white_text"]["AA"]
        white_aaa = checks["white_text"]["AAA"]

        aa_status = click.style("PASS", fg="green") if white_aa else click.style("FAIL", fg="red")
        aaa_status = click.style("PASS", fg="green") if white_aaa else click.style("FAIL", fg="red")

        click.echo(f"  White text - Ratio: {white_ratio}:1  AA: {aa_status}  AAA: {aaa_status}")

        # Black text check
        black_ratio = checks["black_text"]["ratio"]
        black_aa = checks["black_text"]["AA"]
        black_aaa = checks["black_text"]["AAA"]

        aa_status = click.style("PASS", fg="green") if black_aa else click.style("FAIL", fg="red")
        aaa_status = click.style("PASS", fg="green") if black_aaa else click.style("FAIL", fg="red")

        click.echo(f"  Black text - Ratio: {black_ratio}:1  AA: {aa_status}  AAA: {aaa_status}")

    click.echo("\nRecommendation:")
    for color_name, checks in results.items():
        if checks["white_text"]["AA"] and not checks["black_text"]["AA"]:
            click.echo(f"  {color_name}: Use white text")
        elif checks["black_text"]["AA"] and not checks["white_text"]["AA"]:
            click.echo(f"  {color_name}: Use black text")
        elif checks["white_text"]["ratio"] > checks["black_text"]["ratio"]:
            click.echo(f"  {color_name}: White text preferred (higher contrast)")
        else:
            click.echo(f"  {color_name}: Black text preferred (higher contrast)")
