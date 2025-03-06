try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    Image = None
    ImageDraw = None
    ImageFont = None

def generate(palette, output_path, format_type="png"):
    """Generate an image file of the color palette

    Args:
        palette (list): List of RGB color tuples
        output_path (str): Path to save the image file
        format_type (str): Image format ('png' or 'svg')

    Returns:
        str: Path to the generated image file
    """
    if format_type.lower() == "svg":
        return _generate_svg(palette, output_path)
    else:
        return _generate_png(palette, output_path)

def _generate_png(palette, output_path):
    """Generate a PNG image of the color palette

    Args:
        palette (list): List of RGB color tuples
        output_path (str): Path to save the PNG file

    Returns:
        str: Path to the generated PNG file
    """
    if Image is None:
        raise ImportError("Pillow (PIL) library is required for PNG generation. Install with 'pip install pillow'")

    # Define image dimensions
    width = 800
    height = 400
    color_height = 300
    swatch_padding = 2

    # Calculate swatch width
    num_colors = len(palette)
    swatch_width = (width - (num_colors + 1) * swatch_padding) // num_colors

    # Create a new image
    img = Image.new('RGB', (width, height), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)

    # Draw color swatches
    x = swatch_padding
    for color in palette:
        # Draw the color rectangle
        draw.rectangle(
            [(x, swatch_padding), (x + swatch_width, color_height)],
            fill=color,
            outline=(200, 200, 200)
        )

        # Draw color information
        hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        rgb_text = f"RGB: {color[0]}, {color[1]}, {color[2]}"

        # Determine text color (black or white) based on background brightness
        brightness = (color[0] * 299 + color[1] * 587 + color[2] * 114) / 1000
        text_color = (0, 0, 0) if brightness > 128 else (255, 255, 255)

        # Try to load a font or use default
        try:
            font = ImageFont.truetype("Arial", 12)
        except:
            font = ImageFont.load_default()

        # Draw text centered in the swatch
        hex_width, hex_height = draw.textsize(hex_color, font=font) if hasattr(draw, 'textsize') else (len(hex_color) * 7, 14)
        rgb_width, rgb_height = draw.textsize(rgb_text, font=font) if hasattr(draw, 'textsize') else (len(rgb_text) * 7, 14)

        hex_x = x + (swatch_width - hex_width) // 2
        hex_y = color_height + 10

        rgb_x = x + (swatch_width - rgb_width) // 2
        rgb_y = color_height + 30

        draw.text((hex_x, hex_y), hex_color, fill=(0, 0, 0), font=font)
        draw.text((rgb_x, rgb_y), rgb_text, fill=(0, 0, 0), font=font)

        # Move to next position
        x += swatch_width + swatch_padding

    # Save the image
    img.save(output_path)

    return output_path

def _generate_svg(palette, output_path):
    """Generate an SVG image of the color palette

    Args:
        palette (list): List of RGB color tuples
        output_path (str): Path to save the SVG file

    Returns:
        str: Path to the generated SVG file
    """
    # Define dimensions
    width = 800
    height = 400
    color_height = 300
    swatch_padding = 2

    # Calculate swatch width
    num_colors = len(palette)
    swatch_width = (width - (num_colors + 1) * swatch_padding) // num_colors

    # Start SVG content
    svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">\n'
    svg += '  <style>\n'
    svg += '    .hex {{ font-family: Arial, sans-serif; font-size: 12px; }}\n'
    svg += '    .rgb {{ font-family: Arial, sans-serif; font-size: 10px; }}\n'
    svg += '  </style>\n'
    svg += f'  <rect width="{width}" height="{height}" fill="#f0f0f0" />\n'

    # Draw color swatches
    x = swatch_padding
    for i, color in enumerate(palette):
        hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        rgb_text = f"RGB: {color[0]}, {color[1]}, {color[2]}"

        # Determine text color (black or white) based on background brightness
        brightness = (color[0] * 299 + color[1] * 587 + color[2] * 114) / 1000
        text_color = "#000000" if brightness > 128 else "#ffffff"

        # Add the color rectangle
        svg += f'  <rect x="{x}" y="{swatch_padding}" width="{swatch_width}" height="{color_height}" fill="{hex_color}" stroke="#c8c8c8" />\n'

        # Add color name if it's a standard position
        color_name = None
        if i == 0:
            color_name = "Primary"
        elif i == 1:
            color_name = "Secondary"
        elif i == 2:
            color_name = "Accent"

        if color_name:
            svg += f'  <text x="{x + swatch_width/2}" y="{color_height/2 - 10}" fill="{text_color}" text-anchor="middle" class="hex">{color_name}</text>\n'

        # Add hex code centered in the swatch
        svg += f'  <text x="{x + swatch_width/2}" y="{color_height + 20}" fill="#000000" text-anchor="middle" class="hex">{hex_color}</text>\n'

        # Add RGB values
        svg += f'  <text x="{x + swatch_width/2}" y="{color_height + 40}" fill="#000000" text-anchor="middle" class="rgb">{rgb_text}</text>\n'

        # Move to next position
        x += swatch_width + swatch_padding

    # Close SVG
    svg += '</svg>\n'

    # Write to file
    with open(output_path, 'w') as f:
        f.write(svg)

    return output_path
