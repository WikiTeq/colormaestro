import os
try:
    from PIL import Image
except ImportError:
    Image = None

def extract_dominant_color(image_path):
    """Extract the dominant color from an image

    Args:
        image_path (str): Path to image file

    Returns:
        tuple: RGB color tuple (0-255, 0-255, 0-255)
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    if Image is None:
        raise ImportError("Pillow (PIL) library is required for image processing. Install with 'pip install pillow'")

    # Open the image
    img = Image.open(image_path)

    # Resize image to speed up processing
    img = img.copy()
    img.thumbnail((100, 100))

    # Convert to RGB mode if not already
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Get colors from image
    pixels = list(img.getdata())

    # Count occurrences of each color
    color_count = {}
    for pixel in pixels:
        if pixel in color_count:
            color_count[pixel] += 1
        else:
            color_count[pixel] = 1

    # Find the most common color
    dominant_color = max(color_count.items(), key=lambda x: x[1])[0]

    # Skip very dark or very light colors
    r, g, b = dominant_color
    brightness = (r * 299 + g * 587 + b * 114) / 1000

    if brightness < 20 or brightness > 240:
        # Try to find the next most common color that's not too dark/light
        sorted_colors = sorted(color_count.items(), key=lambda x: x[1], reverse=True)

        for color, _ in sorted_colors[1:10]:  # Check top 10 colors
            r, g, b = color
            brightness = (r * 299 + g * 587 + b * 114) / 1000

            if 20 <= brightness <= 240:
                return color

    return dominant_color
