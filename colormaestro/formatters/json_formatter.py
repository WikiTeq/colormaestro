import json
from ..utils import color_conversion

def generate(palette):
    """Generate JSON representation of the color palette

    Args:
        palette (list): List of RGB color tuples

    Returns:
        str: JSON string
    """
    palette_data = {
        "palette": []
    }

    for i, rgb in enumerate(palette):
        hex_code = color_conversion.rgb_to_hex(rgb)
        h, s, v = color_conversion.rgb_to_hsv(rgb)
        h_deg = h * 360
        s_percent = s * 100
        v_percent = v * 100

        color_name = None
        if i == 0:
            color_name = "primary"
        elif i == 1:
            color_name = "secondary"
        elif i == 2:
            color_name = "accent"
        else:
            color_name = f"color-{i+1}"

        color_data = {
            "name": color_name,
            "hex": hex_code,
            "rgb": {
                "r": rgb[0],
                "g": rgb[1],
                "b": rgb[2]
            },
            "hsv": {
                "h": round(h_deg, 2),
                "s": round(s_percent, 2),
                "v": round(v_percent, 2)
            }
        }

        palette_data["palette"].append(color_data)

    return json.dumps(palette_data, indent=2)
