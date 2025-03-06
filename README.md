# ColorMaestro

A comprehensive color palette generation tool for designers and developers.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

ColorMaestro helps you create beautiful, harmonious, and accessible color palettes for your design projects. Generate color schemes using different algorithms, export in multiple formats, and ensure your colors meet accessibility standards.

## Features

- **Multiple Generation Methods**: Create palettes using color harmony rules, monochromatic schemes, accessibility guidelines, mood-based palettes, and UI-optimized color sets
- **Format Options**: Export your palette to CSS, SCSS, Tailwind config, HTML preview, JSON, or terminal output
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

Generate a basic palette from a hex color:

```bash
colormaestro generate --color "#3498db" --method harmony --output palette.html
```

View a palette in the terminal:

```bash
colormaestro generate --color "#e74c3c" --method monochromatic --colors 5 --format terminal
```

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

### Harmony-Based Palettes

Generate palettes based on color theory harmony rules.

```bash
colormaestro generate --color "#9b59b6" --method harmony --harmony-type triadic --colors 6
```

Available harmony types:
- `complementary` - Colors opposite on the color wheel
- `analogous` - Colors adjacent on the color wheel
- `triadic` - Three colors evenly spaced around the color wheel
- `tetradic` - Four colors evenly spaced around the color wheel
- `split-complementary` - Base color plus two colors adjacent to its complement

### Monochromatic Palettes

Create variations of a single color with different lightness and saturation.

```bash
colormaestro generate --color "#2ecc71" --method monochromatic --colors 5
```

### Accessible Palettes

Generate color palettes optimized for accessibility and WCAG compliance.

```bash
colormaestro generate --color "#f39c12" --method accessible --colors 4
```

### Mood-Based Palettes

Create palettes that match a specific mood or feeling.

```bash
colormaestro generate --mood professional --colors 5
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
colormaestro generate --color "#34495e" --method ui --colors 7 --dark-mode
```

## Output Formats

### Terminal Output

Display color palettes directly in your terminal with color previews.

```bash
colormaestro generate --color "#3498db" --format terminal
```

### CSS Variables

Generate CSS custom properties (variables) for your palette.

```bash
colormaestro generate --color "#3498db" --format css --output palette.css
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

Generate SCSS variables and color maps for your palette.

```bash
colormaestro generate --color "#3498db" --format scss --output palette.scss
```

### Tailwind Config

Generate a Tailwind CSS configuration with your palette colors.

```bash
colormaestro generate --color "#3498db" --format tailwind --output tailwind-colors.js
```

### HTML Preview

Generate an HTML file that displays your palette.

```bash
colormaestro generate --color "#3498db" --format html --output palette.html
```

### JSON Format

Export your palette as JSON for integration with other tools.

```bash
colormaestro generate --color "#3498db" --format json --output palette.json
```

### Image Export

Export your palette as a PNG or SVG image.

```bash
colormaestro generate --color "#3498db" --format image --output palette.png
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

```
Usage: colormaestro [OPTIONS] COMMAND [ARGS]...

  ColorMaestro: A color palette generation tool.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  generate  Generate a color palette.
  analyze   Analyze a color or palette.
  convert   Convert colors between formats.
```

### Generate Command

```
Usage: colormaestro generate [OPTIONS]

  Generate a color palette.

Options:
  --color TEXT             Base color in hex format (#RRGGBB).
  --mood [professional|playful|serious|calm|energetic]
                          Generate a palette based on mood.
  --method [harmony|monochromatic|accessible|ui]
                          Color generation method.
  --harmony-type [complementary|analogous|triadic|tetradic|split-complementary]
                          Harmony type when using harmony method.
  --colors INTEGER         Number of colors in the palette.  [default: 5]
  --dark-mode             Generate dark mode optimized palette.
  --format [terminal|css|scss|html|json|tailwind|image]
                          Output format.  [default: terminal]
  --output TEXT           Output file path.
  --show-demo             Show UI component examples.
  --help                  Show this message and exit.
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
