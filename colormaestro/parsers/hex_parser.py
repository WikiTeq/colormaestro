from ..utils import color_conversion

def parse(hex_input):
    """Parse a hex color input

    Args:
        hex_input (str): Hex color code (e.g., '#3A86FF' or '3A86FF')

    Returns:
        tuple: RGB color tuple (0-255, 0-255, 0-255)
    """
    if not color_conversion.is_valid_hex(hex_input):
        raise ValueError(f"Invalid hex color: {hex_input}")

    return color_conversion.hex_to_rgb(hex_input)
