import click
import os

def rgb_to_hex(rgb):
    """Convert RGB tuple to hex string"""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def display(palette, show_demo=False):
    """Display the color palette in the terminal

    Args:
        palette (list): List of RGB color tuples
        show_demo (bool): Whether to show UI component samples
    """
    click.echo("\nColor Palette:\n")

    # Calculate the best text color (black or white) based on color brightness
    def get_text_color(rgb):
        brightness = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
        return "black" if brightness > 128 else "white"

    # Display color info without using hex for bg/fg
    for i, color in enumerate(palette):
        hex_color = rgb_to_hex(color)
        r, g, b = color

        # Create a colored block using Unicode block characters instead of click bg color
        block = "██████████"  # Unicode full blocks

        # Format terminal output with ANSI escape codes
        # This bypasses click's color limitations
        color_display = f"\033[38;2;{r};{g};{b}m{block}\033[0m"

        # Print the color block and info
        click.echo(f"{color_display}  {hex_color}  RGB: {r}, {g}, {b}")

    if show_demo:
        click.echo("\nNote: UI demos are available in HTML output format.")

def display_ui_demo(palette):
    """Display sample UI components using the color palette"""
    click.echo("\nUI Component Samples:\n")

    primary = palette[0]
    primary_hex = rgb_to_hex(primary)
    r, g, b = primary

    # Display a button representation using Unicode characters
    click.echo("Button:")
    button_text = "  BUTTON  "
    button_display = f"\033[48;2;{r};{g};{b}m\033[38;2;255;255;255m{button_text}\033[0m"
    click.echo(button_display)

    # Show color palette as a row of blocks
    if len(palette) >= 3:
        click.echo("\nColor blocks:")
        blocks = ""
        for color in palette:
            r, g, b = color
            blocks += f"\033[48;2;{r};{g};{b}m    \033[0m"
        click.echo(blocks)
