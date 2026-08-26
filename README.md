# ColorMaestro

A comprehensive color palette generation tool for designers and developers.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

ColorMaestro helps you create beautiful, harmonious, and accessible color palettes for your design projects. Generate color schemes using different algorithms, export in multiple formats, and ensure your colors meet accessibility standards.

## Features

- **Multiple Generation Methods**: Create palettes using color harmony rules, monochromatic schemes, accessibility guidelines, mood-based palettes, and UI-optimized color sets
- **Format Options**: Export your palette to CSS, SCSS, Tailwind config, HTML preview, JSON, PNG/SVG images, or terminal output
- **Accessibility Tools**: Check color contrast ratios against WCAG standards
- **CLI Interface**: Generate palettes directly from your terminal
- **Flexible Output**: Use as a library in your Python projects or as a standalone tool

## Installation

### From GitHub

```bash
# Clone the repository
git clone https://github.com/wikiteq/colormaestro.git

# Navigate to the directory
cd colormaestro

# Install the package
pip install -e .
```

### Requirements

- Python 3.8+
- Click (for CLI)
- Pillow (for image generation)
- Jinja2 (for HTML templates)

## Quick Start

### Command Line Usage

Generate a harmony palette from a hex color and save an HTML preview:

```bash
colormaestro "#3498db" --harmony triadic --html palette.html
```

View a monochromatic palette in the terminal:

```bash
colormaestro "#e74c3c" -t mono -n 5
```

If no INPUT is provided, a random palette will be generated:

```bash
colormaestro
```

INPUT can be a hex color (`#3A86FF`), a color name (`sky-blue`), or a path to an image file to extract a dominant color from.

### Python Usage

```python
from colormaestro.generators import harmony
from colormaestro.formatters import terminal, css

# Generate a palette
base_color = (52, 152, 219)  # RGB for #3498db
palette = harmony.generate(base_color, "complementary", 5)

# Display in terminal
terminal.display(palette)

# Generate CSS variables
css_code = css.generate(palette)
print(css_code)
```

## Color Generation Methods

Palette types are selected with `-t/--type`: `ui` (default), `harmony`, `mono`, or `accessible`.

### Harmony-Based Palettes

Generate palettes based on color theory harmony rules.

```bash
colormaestro "#9b59b6" -t harmony --harmony triadic -n 6
```

Available harmony types (via `--harmony`):
- `complementary` - Colors opposite on the color wheel
- `analogous` - Colors adjacent on the color wheel
- `triadic` - Three colors evenly spaced around the color wheel
- `tetradic` - Four colors evenly spaced around the color wheel

### Monochromatic Palettes

Create variations of a single color with different lightness and saturation.

```bash
colormaestro "#2ecc71" -t mono -n 5
```

### Accessible Palettes

Generate color palettes optimized for accessibility and WCAG compliance.

```bash
colormaestro "#f39c12" -t accessible -n 4
```

### Mood-Based Palettes

Create palettes that match a specific mood or feeling.

```bash
colormaestro --mood professional -n 5
```

Available moods:
- `professional`
- `playful`
- `serious`
- `calm`
- `energetic`

### UI-Optimized Palettes

Generate palettes specifically designed for user interfaces with proper contrast.

```bash
colormaestro "#34495e" -t ui -n 7 --dark
```

## Output Formats

Select one or more output formats with `-o/--output` (comma-separated): `terminal` (default), `html`, `css`, `scss`, `tailwind`, `json`, `png`, `svg`.

### Terminal Output

Display color palettes directly in your terminal with color previews.

```bash
colormaestro "#3498db"
```

### CSS Variables

Print CSS custom properties (variables) for your palette.

```bash
colormaestro "#3498db" -o css
```

Example output:

```css
:root {
  --color-primary: #3498db;
  --color-primary-rgb: 52, 152, 219;
  --color-secondary: #db7834;
  --color-secondary-rgb: 219, 120, 52;
  --color-accent: #34db98;
  --color-accent-rgb: 52, 219, 152;

  /* Semantic color mapping */
  --color-background: var(--color-primary);
  --color-text: #000000;
  --color-button: var(--color-secondary);
  --color-border: rgba(var(--color-primary-rgb), 0.2);
  --color-highlight: var(--color-accent);
}
```

### SCSS Variables

Print SCSS variables and color maps for your palette.

```bash
colormaestro "#3498db" -o scss > palette.scss
```

### Tailwind Config

Print a Tailwind CSS configuration with your palette colors.

```bash
colormaestro "#3498db" -o tailwind > tailwind-colors.js
```

### HTML Preview

Generate an HTML file that displays your palette. Use `-o html` for the default filename (`palette.html`) or pass `--html PATH` to choose the location:

```bash
colormaestro "#3498db" -o html
colormaestro "#3498db" --html my-palette.html
```

### JSON Format

Export your palette as JSON for integration with other tools.

```bash
colormaestro "#3498db" -o json > palette.json
```

### Image Export

Export your palette as a PNG or SVG image. Use `-o png`/`-o svg` for default filenames (`palette.png`/`palette.svg`) or pass `--image PATH` to choose the location:

```bash
colormaestro "#3498db" -o png
colormaestro "#3498db" --image my-palette.png
```

## Advanced Usage

### Analyzing Color Contrast

Check if your palette meets WCAG accessibility standards:

```python
from colormaestro.utils import accessibility_utils
from colormaestro.generators import accessible

# Generate an accessible palette
palette = accessible.generate((52, 152, 219), 4)

# Check contrast between all color pairs
results = accessibility_utils.check_contrast(palette)

# Display results
accessibility_utils.display_results(results)
```

You can also check contrast directly from the CLI with `--accessibility`:

```bash
colormaestro "#3498db" --accessibility
```

### Combining Multiple Methods

You can create custom generation workflows:

```python
from colormaestro.generators import mood, harmony
from colormaestro.formatters import css, terminal

# Generate a base color for a specific mood
base_color = mood.generate_base_color("energetic")

# Create a harmonious palette from that base color
palette = harmony.generate(base_color, "analogous", 5)

# Display and export
terminal.display(palette, show_demo=True)
css_code = css.generate(palette)

with open("custom-palette.css", "w") as f:
    f.write(css_code)
```

## Complete CLI Reference

Run `colormaestro --help` for the authoritative list of options:

```
Usage: colormaestro [OPTIONS] [INPUT]

  Color Palette Maestro: Generate stunning color palettes instantly

Options:
  -t, --type [ui|harmony|mono|accessible]
                                  Palette type: ui, harmony, mono, accessible
  --harmony [complementary|analogous|triadic|tetradic]
                                  Harmony type: complementary, analogous,
                                  triadic, tetradic
  -n, --colors INTEGER            Number of colors to generate (default: 5)
  -o, --output TEXT               Output format: terminal, html, css, scss,
                                  tailwind, json, png, svg
  --html TEXT                     Generate HTML preview file
  --image TEXT                    Generate image file of palette
  --mood [professional|playful|serious|calm|energetic]
                                  Color mood
  --dark                          Generate dark mode variant
  --light                         Generate light mode variant
  --demo                          Show sample UI elements with palette
  --accessibility                 Check WCAG contrast compliance
  --copy                          Copy primary color to clipboard
  --help                          Show this message and exit.
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
