import unittest
import os
import json
import tempfile
from unittest.mock import patch, MagicMock
import sys
import io

# Add the parent directory to sys.path to import the colormaestro package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from colormaestro.formatters import css, html, json_formatter, scss, image_formatter, tailwind, terminal
from colormaestro.utils import color_conversion


class TestCSSFormatter(unittest.TestCase):
    """Test the CSS formatter module"""

    def setUp(self):
        # Create a sample color palette for testing
        self.palette = [(58, 134, 255), (242, 179, 79), (255, 32, 122)]
        self.expected_primary = "#3a86ff"
        self.expected_secondary = "#f2b34f"
        self.expected_accent = "#ff207a"

    def test_rgb_to_hex(self):
        """Test RGB to HEX conversion"""
        self.assertEqual(css.rgb_to_hex(self.palette[0]), self.expected_primary)
        self.assertEqual(css.rgb_to_hex(self.palette[1]), self.expected_secondary)
        self.assertEqual(css.rgb_to_hex(self.palette[2]), self.expected_accent)

    def test_generate_basic(self):
        """Test generating CSS variables with a basic palette"""
        result = css.generate(self.palette)

        # Verify the CSS contains key elements
        self.assertIn(":root {", result)
        self.assertIn("--color-primary: #3a86ff;", result)
        self.assertIn("--color-secondary: #f2b34f;", result)
        self.assertIn("--color-accent: #ff207a;", result)
        self.assertIn("--color-primary-rgb: 58, 134, 255;", result)
        self.assertIn("/* Semantic color mapping */", result)

    def test_generate_empty(self):
        """Test generating CSS with an empty palette"""
        result = css.generate([])
        self.assertIn(":root {", result)
        self.assertNotIn("--color-primary", result)
        self.assertNotIn("@media (prefers-color-scheme: dark)", result)

    def test_generate_with_dark_mode(self):
        """Test that dark mode is included when palette has 5+ colors"""
        extended_palette = self.palette + [(211, 218, 229), (140, 145, 153)]
        result = css.generate(extended_palette)
        self.assertIn("@media (prefers-color-scheme: dark)", result)
        self.assertIn("--color-text: #ffffff;", result)
        self.assertIn("--color-background: #121212;", result)


class TestHTMLFormatter(unittest.TestCase):
    """Test the HTML formatter module"""

    def setUp(self):
        self.palette = [(58, 134, 255), (242, 179, 79), (255, 32, 122)]
        self.temp_dir = tempfile.mkdtemp()
        self.output_path = os.path.join(self.temp_dir, "palette.html")

    def tearDown(self):
        # Clean up temporary files
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

    @patch('jinja2.Environment')
    def test_generate_html(self, mock_env):
        """Test HTML generation with mocked Jinja2"""
        # Setup mock
        mock_template = MagicMock()
        mock_env.return_value.get_template.return_value = mock_template
        mock_template.render.return_value = "<html>Test Content</html>"

        # Run the generate function
        result = html.generate(self.palette, self.output_path)

        # Verify the template was loaded and rendered
        mock_env.return_value.get_template.assert_called_with('html_preview.html')
        mock_template.render.assert_called_once()

        # Verify file was created
        self.assertTrue(os.path.exists(self.output_path))
        self.assertEqual(result, self.output_path)

    def test_color_formatting(self):
        """Test actual HTML generation without mocking"""
        try:
            result = html.generate(self.palette, self.output_path)

            # Check that file exists and has content
            self.assertTrue(os.path.exists(result))
            with open(result, 'r') as f:
                content = f.read()

            # Check for key expected content
            self.assertIn("<!DOCTYPE html>", content)
            self.assertIn("#3a86ff", content)  # Primary color hex
            self.assertIn("RGB: 58, 134, 255", content)  # Primary color RGB
        except ImportError:
            self.skipTest("Jinja2 not installed")


class TestJSONFormatter(unittest.TestCase):
    """Test the JSON formatter module"""

    def setUp(self):
        self.palette = [(58, 134, 255), (242, 179, 79), (255, 32, 122)]

    def test_generate_json(self):
        """Test generating JSON representation of a palette"""
        result = json_formatter.generate(self.palette)
        data = json.loads(result)

        # Verify structure
        self.assertIn("palette", data)
        self.assertEqual(len(data["palette"]), 3)

        # Verify color data
        self.assertEqual(data["palette"][0]["name"], "primary")
        self.assertEqual(data["palette"][0]["hex"], "#3a86ff")
        self.assertEqual(data["palette"][0]["rgb"]["r"], 58)
        self.assertEqual(data["palette"][1]["name"], "secondary")
        self.assertEqual(data["palette"][2]["name"], "accent")

    def test_generate_empty(self):
        """Test with empty palette"""
        result = json_formatter.generate([])
        data = json.loads(result)
        self.assertIn("palette", data)
        self.assertEqual(len(data["palette"]), 0)


class TestSCSSFormatter(unittest.TestCase):
    """Test the SCSS formatter module"""

    def setUp(self):
        self.palette = [(58, 134, 255), (242, 179, 79), (255, 32, 122)]

    def test_rgb_to_hex(self):
        """Test RGB to HEX conversion"""
        self.assertEqual(scss.rgb_to_hex(self.palette[0]), "#3a86ff")

    def test_generate_scss(self):
        """Test generating SCSS variables"""
        result = scss.generate(self.palette)

        # Check for SCSS variables
        self.assertIn("$primary: #3a86ff;", result)
        self.assertIn("$secondary: #f2b34f;", result)
        self.assertIn("$accent: #ff207a;", result)

        # Check for SCSS map
        self.assertIn("$colors: (", result)
        self.assertIn("  'primary': #3a86ff,", result)

        # Check for utility functions
        self.assertIn("@function rgba-palette", result)
        self.assertIn("@mixin text-on-color", result)


class TestImageFormatter(unittest.TestCase):
    """Test the image formatter module"""

    def setUp(self):
        self.palette = [(58, 134, 255), (242, 179, 79), (255, 32, 122)]
        self.temp_dir = tempfile.mkdtemp()
        self.png_path = os.path.join(self.temp_dir, "palette.png")
        self.svg_path = os.path.join(self.temp_dir, "palette.svg")

    def tearDown(self):
        # Clean up temporary files
        for path in [self.png_path, self.svg_path]:
            if os.path.exists(path):
                os.remove(path)

    def test_generate_svg(self):
        """Test generating SVG image"""
        result = image_formatter.generate(self.palette, self.svg_path, "svg")

        # Verify file exists
        self.assertTrue(os.path.exists(result))

        # Check content
        with open(result, 'r') as f:
            content = f.read()
            self.assertIn("<svg", content)
            self.assertIn("#3a86ff", content)  # Primary color
            self.assertIn("Primary", content)  # Label

    @unittest.skipIf(image_formatter.Image is None, "PIL not installed")
    def test_generate_png(self):
        """Test generating PNG image (requires PIL)"""
        result = image_formatter.generate(self.palette, self.png_path, "png")

        # Verify file exists and is a valid size
        self.assertTrue(os.path.exists(result))
        self.assertTrue(os.path.getsize(result) > 0)


class TestTailwindFormatter(unittest.TestCase):
    """Test the Tailwind CSS formatter module"""

    def setUp(self):
        self.palette = [(58, 134, 255), (242, 179, 79), (255, 32, 122)]

    def test_rgb_to_hex(self):
        """Test RGB to HEX conversion"""
        self.assertEqual(tailwind.rgb_to_hex(self.palette[0]), "#3a86ff")

    def test_generate_tailwind(self):
        """Test generating Tailwind config"""
        result = tailwind.generate(self.palette)

        # Check basic structure
        self.assertIn("// tailwind.config.js", result)
        self.assertIn("module.exports = {", result)

        # Check color definitions
        self.assertIn("primary: {", result)
        self.assertIn("DEFAULT: '#3a86ff'", result)
        self.assertIn("secondary: '#f2b34f'", result)
        self.assertIn("accent: '#ff207a'", result)

        # Check for shade generation
        self.assertIn("'50':", result)
        self.assertIn("'900':", result)


class TestTerminalFormatter(unittest.TestCase):
    """Test the terminal formatter module"""

    def setUp(self):
        self.palette = [(58, 134, 255), (242, 179, 79), (255, 32, 122)]

    def test_rgb_to_hex(self):
        """Test RGB to HEX conversion"""
        self.assertEqual(terminal.rgb_to_hex(self.palette[0]), "#3a86ff")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('click.echo')
    def test_display(self, mock_echo, mock_stdout):
        """Test terminal display function"""
        terminal.display(self.palette)

        # Verify click.echo was called multiple times
        self.assertTrue(mock_echo.call_count >= 3)

        # Verify each color is mentioned in the output
        calls = [call[0][0] for call in mock_echo.call_args_list]

        hex_primary = "#3a86ff"
        hex_secondary = "#f2b34f"
        hex_accent = "#ff207a"

        primary_found = False
        secondary_found = False
        accent_found = False

        for call_arg in calls:
            if isinstance(call_arg, str):
                if hex_primary in call_arg:
                    primary_found = True
                if hex_secondary in call_arg:
                    secondary_found = True
                if hex_accent in call_arg:
                    accent_found = True

        self.assertTrue(primary_found)
        self.assertTrue(secondary_found)
        self.assertTrue(accent_found)

    @patch('click.echo')
    def test_display_with_demo(self, mock_echo):
        """Test terminal display with demo enabled"""
        terminal.display(self.palette, show_demo=True)

        # Verify that the demo message is shown
        demo_shown = False
        for call in mock_echo.call_args_list:
            if "UI demos are available in HTML output format" in str(call):
                demo_shown = True
                break

        self.assertTrue(demo_shown)


if __name__ == '__main__':
    unittest.main()
