import random
import colorsys
import re

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple

    Args:
        hex_color (str): Hex color code (e.g., '#3A86FF' or '3A86FF')

    Returns:
        tuple: RGB color tuple (0-255, 0-255, 0-255)
    """
    # Remove hash if present
    hex_color = hex_color.lstrip('#')

    # Handle shorthand hex notation (e.g., #FFF)
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])

    # Convert to RGB
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """Convert RGB tuple to hex string

    Args:
        rgb (tuple): RGB color tuple (0-255, 0-255, 0-255)

    Returns:
        str: Hex color code with leading hash
    """
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def rgb_to_hsv(rgb):
    """Convert RGB tuple to HSV tuple

    Args:
        rgb (tuple): RGB color tuple (0-255, 0-255, 0-255)

    Returns:
        tuple: HSV color tuple (0-1, 0-1, 0-1)
    """
    r, g, b = [x/255.0 for x in rgb]
    return colorsys.rgb_to_hsv(r, g, b)

def hsv_to_rgb(hsv):
    """Convert HSV tuple to RGB tuple

    Args:
        hsv (tuple): HSV color tuple (0-1, 0-1, 0-1)

    Returns:
        tuple: RGB color tuple (0-255, 0-255, 0-255)
    """
    r, g, b = colorsys.hsv_to_rgb(*hsv)
    return (int(r*255), int(g*255), int(b*255))

def rgb_to_hsl(rgb):
    """Convert RGB tuple to HSL tuple

    Args:
        rgb (tuple): RGB color tuple (0-255, 0-255, 0-255)

    Returns:
        tuple: HSL color tuple (0-1, 0-1, 0-1)
    """
    r, g, b = [x/255.0 for x in rgb]
    return colorsys.rgb_to_hls(r, g, b)

def hsl_to_rgb(hsl):
    """Convert HSL tuple to RGB tuple

    Args:
        hsl (tuple): HSL color tuple (0-1, 0-1, 0-1)

    Returns:
        tuple: RGB color tuple (0-255, 0-255, 0-255)
    """
    h, s, l = hsl
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return (int(r*255), int(g*255), int(b*255))

def random_color():
    """Generate a random vibrant color

    Returns:
        tuple: RGB color tuple (0-255, 0-255, 0-255)
    """
    # Generate a random hue (0-1)
    h = random.random()

    # Use high saturation and value for vibrant colors
    s = random.uniform(0.7, 1.0)
    v = random.uniform(0.8, 1.0)

    # Convert to RGB
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (int(r*255), int(g*255), int(b*255))

def is_valid_hex(hex_str):
    """Check if string is a valid hex color

    Args:
        hex_str (str): String to check

    Returns:
        bool: True if valid hex color, False otherwise
    """
    pattern = r'^#?([A-Fa-f0-9]{3}|[A-Fa-f0-9]{6})$'
    return bool(re.match(pattern, hex_str))

def adjust_brightness(rgb, factor):
    """Adjust the brightness of an RGB color

    Args:
        rgb (tuple): RGB color tuple (0-255, 0-255, 0-255)
        factor (float): Factor to adjust brightness by (0-2)
                        < 1 darkens, > 1 lightens

    Returns:
        tuple: Adjusted RGB color tuple
    """
    r, g, b = rgb

    # Convert to HSL for easier brightness adjustment
    h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)

    # Adjust lightness
    l = max(0, min(1, l * factor))

    # Convert back to RGB
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return (int(r*255), int(g*255), int(b*255))

def get_color_info(rgb):
    """Get comprehensive color information

    Args:
        rgb (tuple): RGB color tuple (0-255, 0-255, 0-255)

    Returns:
        dict: Color information
    """
    r, g, b = rgb
    hex_code = rgb_to_hex(rgb)
    h, s, v = rgb_to_hsv(rgb)
    h_deg = h * 360

    return {
        'hex': hex_code,
        'rgb': rgb,
        'r': r,
        'g': g,
        'b': b,
        'hsv': (h, s, v),
        'h': h_deg,
        's_percent': s * 100,
        'v_percent': v * 100,
    }
