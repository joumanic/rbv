import unittest
from PIL import Image, ImageDraw
from io import BytesIO
from scripts.utility import hex_to_rgb, draw_rounded_rectangle

class TestImageUtils(unittest.TestCase):
    
    # Tests for hex_to_rgb function
    def test_hex_to_rgb_standard(self):
        # Standard hex colors
        self.assertEqual(hex_to_rgb("#FFFFFF"), (255, 255, 255))
        self.assertEqual(hex_to_rgb("#000000"), (0, 0, 0))
        self.assertEqual(hex_to_rgb("#FF5733"), (255, 87, 51))
    
    def test_hex_to_rgb_without_hash(self):
        # Hex colors without '#'
        self.assertEqual(hex_to_rgb("FFFFFF"), (255, 255, 255))
        self.assertEqual(hex_to_rgb("000000"), (0, 0, 0))
        self.assertEqual(hex_to_rgb("FF5733"), (255, 87, 51))

    def test_hex_to_rgb_invalid(self):
        # Invalid hex color should raise a ValueError
        with self.assertRaises(ValueError):
            hex_to_rgb("#GGGGGG")  # Invalid hex characters
        with self.assertRaises(ValueError):
            hex_to_rgb("#FFF")  # Incorrect length for hex color

    # Tests for draw_rounded_rectangle function
    def test_draw_rounded_rectangle(self):
        # Create a test image and draw object
        img = Image.new("RGB", (100, 100), "white")
        draw = ImageDraw.Draw(img)

        # Draw a rounded rectangle and verify output visually
        try:
            draw_rounded_rectangle(draw, (10, 10, 90, 90), 20, fill="blue")
        except Exception as e:
            self.fail(f"draw_rounded_rectangle raised an unexpected exception: {e}")

        # Since the function doesn't return values, we rely on visual/manual inspection here.
        # For automated testing, consider verifying individual draw calls if using a mock.

    def test_draw_rounded_rectangle_zero_radius(self):
        # Create a test image and draw object
        img = Image.new("RGB", (100, 100), "white")
        draw = ImageDraw.Draw(img)

        # Draw a rectangle with zero radius (should be a regular rectangle)
        try:
            draw_rounded_rectangle(draw, (10, 10, 90, 90), 0, fill="red")
        except Exception as e:
            self.fail(f"draw_rounded_rectangle with zero radius raised an unexpected exception: {e}")

    def test_draw_rounded_rectangle_large_radius(self):
        # Test with radius greater than half of the rectangle's smallest side
        img = Image.new("RGB", (100, 100), "white")
        draw = ImageDraw.Draw(img)

        # Draw a fully rounded rectangle (radius = 50, should cover corners)
        try:
            draw_rounded_rectangle(draw, (10, 10, 90, 90), 50, fill="green")
        except Exception as e:
            self.fail(f"draw_rounded_rectangle with large radius raised an unexpected exception: {e}")

if __name__ == "__main__":
    unittest.main()
