import pytest
import random
from unittest.mock import patch

from colormaestro.generators import harmony as harmony_generator
from colormaestro.generators import ui_palette
from colormaestro.generators import monochromatic
from colormaestro.generators import accessible
from colormaestro.generators import mood as mood_generator
from colormaestro.utils import color_conversion

# Sample RGB colors for testing
SAMPLE_COLORS = {
    'blue': (58, 134, 255),     # #3A86FF
    'red': (255, 59, 48),       # #FF3B30
    'green': (40, 205, 65),     # #28CD41
    'yellow': (255, 204, 0),    # #FFCC00
    'purple': (175, 82, 222),   # #AF52DE
    'black': (0, 0, 0),         # #000000
    'white': (255, 255, 255),   # #FFFFFF
}

class TestHarmonyGenerator:
    """Tests for the harmony generator module"""

    def test_complementary(self):
        """Test complementary harmony generation"""
        base_color = SAMPLE_COLORS['blue']
        palette = harmony_generator.generate(base_color, "complementary", 5)

        # Check that the palette has the correct length
        assert len(palette) == 5

        # Check that the base color is in the palette
        assert base_color in palette

        # Check that the palette contains unique colors
        assert len(set(palette)) >= 2

    def test_analogous(self):
        """Test analogous harmony generation"""
        base_color = SAMPLE_COLORS['red']
        palette = harmony_generator.generate(base_color, "analogous", 4)

        # Check that the palette has the correct length
        assert len(palette) == 4

        # Check that the base color is in the palette
        assert base_color in palette

        # Check that the palette contains unique colors
        assert len(set(palette)) >= 3

    def test_triadic(self):
        """Test triadic harmony generation"""
        base_color = SAMPLE_COLORS['green']
        palette = harmony_generator.generate(base_color, "triadic", 6)

        # Check that the palette has the correct length
        assert len(palette) == 6

        # Check that the base color is in the palette
        assert base_color in palette

        # Check that the palette contains unique colors
        assert len(set(palette)) >= 3

    def test_tetradic(self):
        """Test tetradic harmony generation"""
        base_color = SAMPLE_COLORS['purple']
        palette = harmony_generator.generate(base_color, "tetradic", 7)

        # Check that the palette has the correct length
        assert len(palette) == 7

        # Check that the base color is in the palette
        assert base_color in palette

        # Check that the palette contains unique colors
        assert len(set(palette)) >= 4

class TestMonochromaticGenerator:
    """Tests for the monochromatic generator module"""

    def test_basic_generation(self):
        """Test basic monochromatic palette generation"""
        base_color = SAMPLE_COLORS['blue']
        palette = monochromatic.generate(base_color, 5)

        # Check that the palette has the correct length
        assert len(palette) == 5

        # Check that all colors have the same hue
        for color in palette:
            base_h = color_conversion.rgb_to_hsv(base_color)[0]
            color_h = color_conversion.rgb_to_hsv(color)[0]
            # Allow small differences due to rounding
            assert abs(base_h - color_h) < 0.01

    def test_min_colors(self):
        """Test with minimum number of colors"""
        base_color = SAMPLE_COLORS['red']
        palette = monochromatic.generate(base_color, 1)

        # Check that the palette has at least one color
        assert len(palette) >= 1

    def test_max_colors(self):
        """Test with a large number of colors"""
        base_color = SAMPLE_COLORS['green']
        palette = monochromatic.generate(base_color, 20)

        # Check that the palette has the correct length
        assert len(palette) == 20

        # Check that we have variation in the colors
        saturations = set()
        values = set()
        for color in palette:
            _, s, v = color_conversion.rgb_to_hsv(color)
            saturations.add(round(s, 2))
            values.add(round(v, 2))

        # There should be some variation in saturation or value
        assert len(saturations) > 1 or len(values) > 1

class TestAccessibleGenerator:
    """Tests for the accessible color generator module"""

    def test_basic_generation(self):
        """Test basic accessible palette generation"""
        base_color = SAMPLE_COLORS['blue']
        palette = accessible.generate(base_color, 5)

        # Check that the palette has the correct length
        assert len(palette) == 5

        # Check that the base color is in the palette
        assert base_color in palette

        # Check color contrast for at least some pairs
        from colormaestro.utils import accessibility_utils
        results = accessibility_utils.check_contrast(palette)

        # There should be at least some pairs with good contrast
        assert any(result['passes_aa'] for result in results)

    def test_black_white_contrast(self):
        """Test that black and white have maximum contrast"""
        base_color = SAMPLE_COLORS['black']
        palette = accessible.generate(base_color, 4)

        # Check if white is in the palette for maximum contrast
        assert (255, 255, 255) in palette or any(sum(color) > 700 for color in palette)

    def test_different_base_colors(self):
        """Test generation with different base colors"""
        for color_name, base_color in SAMPLE_COLORS.items():
            palette = accessible.generate(base_color, 4)

            # Check that the palette has the correct length
            assert len(palette) == 4

            # Check that all colors are valid RGB tuples
            for color in palette:
                assert len(color) == 3
                assert all(0 <= c <= 255 for c in color)

class TestUIGenerator:
    """Tests for the UI palette generator module"""

    def test_basic_generation(self):
        """Test basic UI palette generation"""
        base_color = SAMPLE_COLORS['blue']
        palette = ui_palette.generate(base_color, 5)

        # Check that the palette has the correct length
        assert len(palette) == 5

        # Check that the base color is in the palette
        assert base_color in palette

        # Check that all colors are valid RGB tuples
        for color in palette:
            assert len(color) == 3
            assert all(0 <= c <= 255 for c in color)

    def test_dark_mode(self):
        """Test dark mode UI palette generation"""
        base_color = SAMPLE_COLORS['blue']
        palette = ui_palette.generate(base_color, 5, dark=True)

        # Check that the palette has the correct length
        assert len(palette) == 5

        # In dark mode, we expect some darker colors
        dark_colors = [color for color in palette if sum(color) < 384]  # Average < 128 per channel
        assert len(dark_colors) >= 2

    def test_accessibility(self):
        """Test that UI palettes have good contrast"""
        base_color = SAMPLE_COLORS['purple']
        palette = ui_palette.generate(base_color, 5)

        # Check contrast between at least some pairs
        from colormaestro.utils import accessibility_utils
        results = accessibility_utils.check_contrast(palette)

        # There should be at least some pairs with good contrast
        assert any(result['passes_aa'] for result in results)

class TestMoodGenerator:
    """Tests for the mood-based generator module"""

    @patch('random.choice')
    @patch('random.uniform')
    def test_mood_profiles(self, mock_uniform, mock_choice):
        """Test that different moods produce expected colors"""

        # Test all available moods
        moods = ["professional", "playful", "serious", "calm", "energetic"]

        for mood in moods:
            # Mock the random functions to return predictable values
            mock_choice.return_value = [0.5, 0.6]  # A hue range
            mock_uniform.side_effect = [0.55, 0.7, 0.8]  # h, s, v values

            color = mood_generator.generate_base_color(mood)

            # Check that we get a valid RGB color
            assert len(color) == 3
            assert all(0 <= c <= 255 for c in color)

    def test_invalid_mood(self):
        """Test handling of invalid mood"""
        with pytest.raises(ValueError):
            mood_generator.generate_base_color("nonexistent_mood")

    def test_generate_multiple_moods(self):
        """Test generating colors for different moods"""
        moods = ["professional", "playful", "serious", "calm", "energetic"]
        colors = {}

        for mood in moods:
            colors[mood] = mood_generator.generate_base_color(mood)

        # Check that all moods produced valid colors
        for mood, color in colors.items():
            assert len(color) == 3
            assert all(0 <= c <= 255 for c in color)

        # The colors should generally be different for different moods
        unique_colors = set(colors.values())
        assert len(unique_colors) >= 3  # With random generation, we might get some duplicates

if __name__ == "__main__":
    pytest.main(["-v"])
