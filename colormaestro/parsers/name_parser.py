import json
import os
import random
from ..utils import color_conversion

# Dictionary of common color names to hex values
COLOR_NAMES = {
    # Basic colors
    "black": "#000000",
    "white": "#FFFFFF",
    "red": "#FF0000",
    "green": "#00FF00",
    "blue": "#0000FF",
    "yellow": "#FFFF00",
    "cyan": "#00FFFF",
    "magenta": "#FF00FF",
    "purple": "#800080",
    "orange": "#FFA500",
    "pink": "#FFC0CB",
    "gray": "#808080",
    "brown": "#A52A2A",

    # Extended colors
    "navy": "#000080",
    "teal": "#008080",
    "maroon": "#800000",
    "olive": "#808000",
    "lime": "#00FF00",
    "aqua": "#00FFFF",
    "silver": "#C0C0C0",
    "gold": "#FFD700",
    "indigo": "#4B0082",
    "violet": "#EE82EE",
    "coral": "#FF7F50",
    "salmon": "#FA8072",
    "turquoise": "#40E0D0",
    "skyblue": "#87CEEB",
    "khaki": "#F0E68C",
    "crimson": "#DC143C",

    # Branded colors
    "facebook-blue": "#1877F2",
    "twitter-blue": "#1DA1F2",
    "instagram-purple": "#C13584",
    "snapchat-yellow": "#FFFC00",
    "youtube-red": "#FF0000",
    "whatsapp-green": "#25D366",
    "linkedin-blue": "#0077B5",
    "slack-purple": "#4A154B",
}

# Add variations
COLOR_NAMES.update({
    "sky-blue": COLOR_NAMES["skyblue"],
    "sky": COLOR_NAMES["skyblue"],
    "blood-red": "#8B0000",
    "forest-green": "#228B22",
    "sea-green": "#2E8B57",
    "hot-pink": "#FF69B4",
    "deep-purple": "#6A0DAD",
    "royal-blue": "#4169E1",
    "midnight-blue": "#191970",
    "dark-green": "#006400",
    "light-blue": "#ADD8E6",
    "dark-gray": "#A9A9A9",
    "light-gray": "#D3D3D3",
})

def get_color_name_dict():
    """Get the color name dictionary

    Returns:
        dict: Dictionary of color names to hex values
    """
    return COLOR_NAMES

def parse(color_name):
    """Parse a color name to RGB

    Args:
        color_name (str): Color name (e.g., 'sky-blue', 'red')

    Returns:
        tuple: RGB color tuple (0-255, 0-255, 0-255)
    """
    # Convert to lowercase and replace spaces with dashes
    color_name = color_name.lower().replace(' ', '-')

    # Check if color name exists in our dictionary
    if color_name in COLOR_NAMES:
        hex_value = COLOR_NAMES[color_name]
        return color_conversion.hex_to_rgb(hex_value)

    # Handle fuzzy matching for similar color names
    best_match = None
    best_score = 0

    for name in COLOR_NAMES:
        # Simple scoring based on substring matching
        if color_name in name or name in color_name:
            score = len(set(color_name) & set(name))
            if score > best_score:
                best_score = score
                best_match = name

    if best_match and best_score > len(color_name) / 2:
        hex_value = COLOR_NAMES[best_match]
        return color_conversion.hex_to_rgb(hex_value)

    # If no match found, generate a random color with the seed of the name
    random.seed(color_name)
    h = random.random()  # random hue
    s = random.uniform(0.6, 1.0)  # high saturation
    v = random.uniform(0.7, 1.0)  # high value

    # Convert HSV to RGB
    r, g, b = color_conversion.hsv_to_rgb((h, s, v))
    return (r, g, b)
