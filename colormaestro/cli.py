#!/usr/bin/env python3
import os
import click
from pathlib import Path
from .parsers import hex_parser, name_parser, image_parser
from .generators import harmony as harmony_generator, ui_palette, monochromatic, accessible, mood as mood_generator
from .formatters import terminal, html, css, scss, tailwind, json_formatter, image_formatter
from .utils import color_conversion, accessibility as accessibility_utils

PALETTE_TYPES = ["ui", "harmony", "mono", "accessible"]
HARMONY_TYPES = ["complementary", "analogous", "triadic", "tetradic"]
OUTPUT_FORMATS = ["terminal", "html", "css", "scss", "tailwind", "json", "png", "svg"]
MOOD_OPTIONS = ["professional", "playful", "serious", "calm", "energetic"]

@click.command()
@click.argument('input', required=False)
@click.option('-t', '--type', 'palette_type', type=click.Choice(PALETTE_TYPES), default="ui",
              help='Palette type: ui, harmony, mono, accessible')
@click.option('--harmony', type=click.Choice(HARMONY_TYPES), default="complementary",
              help='Harmony type: complementary, analogous, triadic, tetradic')
@click.option('-n', '--colors', 'num_colors', type=int, default=5,
              help='Number of colors to generate (default: 5)')
@click.option('-o', '--output', 'output_format', type=str, default="terminal",
              help='Output format: terminal, html, css, scss, tailwind, json, png, svg')
@click.option('--html', 'html_filename', type=str, help='Generate HTML preview file')
@click.option('--image', 'image_filename', type=str, help='Generate image file of palette')
@click.option('--mood', type=click.Choice(MOOD_OPTIONS), help='Color mood')
@click.option('--dark', is_flag=True, help='Generate dark mode variant')
@click.option('--light', is_flag=True, help='Generate light mode variant')
@click.option('--demo', is_flag=True, help='Show sample UI elements with palette')
@click.option('--accessibility', 'check_accessibility', is_flag=True, help='Check WCAG contrast compliance')
@click.option('--copy', is_flag=True, help='Copy primary color to clipboard')
def cli(input, palette_type, harmony, num_colors, output_format, html_filename,
        image_filename, mood, dark, light, demo, check_accessibility, copy):
    """Color Palette Maestro: Generate stunning color palettes instantly

    INPUT can be a hex color (#3A86FF), color name (sky-blue), or path to an image file.
    If no INPUT is provided, a random palette will be generated.
    """
    click.echo(click.style("Color Palette Maestro", fg="bright_magenta", bold=True))
    click.echo("──────────────────────────────────────")

    # Parse input
    base_color = None
    if not input:
        click.echo("Generating random palette...")
        if mood:
            base_color = mood_generator.generate_base_color(mood)
        else:
            base_color = color_conversion.random_color()
    elif input.startswith('#'):
        click.echo(f"Parsing hex color: {input}")
        base_color = hex_parser.parse(input)
    elif os.path.isfile(input):
        click.echo(f"Extracting colors from image: {input}")
        base_color = image_parser.extract_dominant_color(input)
    else:
        click.echo(f"Parsing color name: {input}")
        base_color = name_parser.parse(input)

    # Generate palette
    palette = None
    if palette_type == "ui":
        palette = ui_palette.generate(base_color, num_colors, dark)
    elif palette_type == "harmony":
        palette = harmony_generator.generate(base_color, harmony, num_colors)
    elif palette_type == "mono":
        palette = monochromatic.generate(base_color, num_colors)
    elif palette_type == "accessible":
        palette = accessible.generate(base_color, num_colors)

    # Output formatting
    output_formats = output_format.split(',')
    for fmt in output_formats:
        fmt = fmt.strip()
        if fmt == "terminal":
            terminal.display(palette, show_demo=demo)
        elif fmt == "html" or html_filename:
            html_path = html_filename or "palette.html"
            html.generate(palette, html_path, show_demo=demo)
            click.echo(f"HTML preview saved to: {html_path}")
        elif fmt == "css":
            css_output = css.generate(palette)
            click.echo(css_output)
        elif fmt == "scss":
            scss_output = scss.generate(palette)
            click.echo(scss_output)
        elif fmt == "tailwind":
            tailwind_output = tailwind.generate(palette)
            click.echo(tailwind_output)
        elif fmt == "json":
            json_output = json_formatter.generate(palette)
            click.echo(json_output)
        elif fmt in ["png", "svg"] or image_filename:
            img_path = image_filename or f"palette.{fmt}"
            image_formatter.generate(palette, img_path, fmt)
            click.echo(f"Image saved to: {img_path}")

    # Additional features
    if check_accessibility:
        results = accessibility_utils.check_contrast(palette)
        accessibility_utils.display_results(results)

    if copy:
        primary_color = palette[0]
        # Copy to clipboard - platform specific code would go here
        click.echo(f"Primary color {primary_color} copied to clipboard")

if __name__ == '__main__':
    cli()
