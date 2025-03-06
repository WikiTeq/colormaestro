import random
from ..utils import color_conversion

# Define mood profiles with HSV ranges
MOOD_PROFILES = {
    "professional": {
        "h_range": [(0.55, 0.65), (0.2, 0.3)],  # Blues and greens
        "s_range": (0.3, 0.7),  # Medium saturation
        "v_range": (0.6, 0.9),  # Medium to high value
    },
    "playful": {
        "h_range": [(0.05, 0.15), (0.3, 0.4), (0.7, 0.85)],  # Oranges, greens, purples
        "s_range": (0.6, 1.0),  # High saturation
        "v_range": (0.8, 1.0),  # High value
    },
    "serious": {
        "h_range": [(0.55, 0.7), (0.0, 0.1)],  # Blues and reds
        "s_range": (0.3, 0.6),  # Medium saturation
        "v_range": (0.4, 0.7),  # Medium to low value
    },
    "calm": {
        "h_range": [(0.4, 0.55), (0.7, 0.85)],  # Greens and purples
        "s_range": (0.2, 0.5),  # Lower saturation
        "v_range": (0.7, 0.9),  # Medium to high value
    },
    "energetic": {
        "h_range": [(0.95, 1.0), (0.0, 0.15), (0.4, 0.5)],  # Reds, oranges, greens
        "s_range": (0.8, 1.0),  # High saturation
        "v_range": (0.8, 1.0),  # High value
    },
}

def generate_base_color(mood):
    """Generate a base color that fits a specified mood

    Args:
        mood (str): Mood name ('professional', 'playful', 'serious', 'calm', 'energetic')

    Returns:
        tuple: RGB color tuple (0-255, 0-255, 0-255)
    """
    if mood not in MOOD_PROFILES:
        raise ValueError(f"Unknown mood: {mood}. Valid options are: {', '.join(MOOD_PROFILES.keys())}")

    profile = MOOD_PROFILES[mood]

    # Randomly select one of the hue ranges
    h_range = random.choice(profile["h_range"])

    # Generate random HSV values within the mood's ranges
    h = random.uniform(*h_range)
    s = random.uniform(*profile["s_range"])
    v = random.uniform(*profile["v_range"])

    # Convert to RGB
    return color_conversion.hsv_to_rgb((h, s, v))
