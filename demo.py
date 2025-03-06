#!/usr/bin/env python3
from colormaestro.parsers import hex_parser, name_parser
from colormaestro.generators import harmony, ui_palette
from colormaestro.formatters import terminal, css

def main():
    # Get a color
    hex_color = "#3A86FF"  # You can change this to any color you like
    print(f"Starting with color: {hex_color}")

    # Parse the hex color
    rgb_color = hex_parser.parse(hex_color)

    # Generate a harmony palette
    harmony_type = "triadic"
    num_colors = 5
    palette = harmony.generate(rgb_color, harmony_type, num_colors)

    # Display in terminal
    print(f"\n{harmony_type.title()} harmony palette with {num_colors} colors:")
    terminal.display(palette, show_demo=True)

    # Generate UI palette from a color name
    color_name = "coral"
    rgb_from_name = name_parser.parse(color_name)
    ui_palette_result = ui_palette.generate(rgb_from_name, 6)

    print(f"\nUI palette from color name '{color_name}':")
    terminal.display(ui_palette_result)

    # Generate CSS
    css_code = css.generate(palette)
    with open("demo_palette.css", "w") as f:
        f.write(css_code)
    print("\nCSS variables saved to demo_palette.css")

if __name__ == "__main__":
    main()
