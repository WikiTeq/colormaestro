import os
import jinja2
from ..utils import color_conversion

def generate(palette, output_path, show_demo=False):
    """Generate HTML preview of the color palette

    Args:
        palette (list): List of RGB color tuples
        output_path (str): Path to save the HTML file
        show_demo (bool): Whether to show UI component samples

    Returns:
        str: Path to the generated HTML file
    """
    # Get the directory containing this script
    package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    templates_dir = os.path.join(package_dir, 'templates')

    # Set up Jinja environment
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(templates_dir),
        autoescape=jinja2.select_autoescape(['html', 'xml'])
    )

    # Load the template
    template = env.get_template('html_preview.html')

    # Prepare color data
    colors = []
    for i, rgb in enumerate(palette):
        name = None
        if i == 0:
            name = "Primary"
        elif i == 1:
            name = "Secondary"
        elif i == 2:
            name = "Accent"

        hex_code = color_conversion.rgb_to_hex(rgb)
        colors.append({
            'hex': hex_code,
            'r': rgb[0],
            'g': rgb[1],
            'b': rgb[2],
            'name': name
        })

    # Render the template
    html_content = template.render(
        palette=colors,
        show_demo=show_demo
    )

    # Ensure directory exists
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # Write to file
    with open(output_path, 'w') as f:
        f.write(html_content)

    return output_path
