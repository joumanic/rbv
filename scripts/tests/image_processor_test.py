import unittest
from unittest.mock import patch, MagicMock
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from scripts.image_processor import ImageProcessor


class TestImageProcessor(unittest.TestCase):

    def setUp(self):
        # Initialize ImageProcessor instance and sample image
        self.processor = ImageProcessor()
        self.sample_image = Image.new("RGB", (100, 100), "blue")  # Create a simple image for testing

    def test_convert_image_success(self):
        img = self.sample_image.copy()
        result = self.processor.convert_image(img, "L")
        self.assertEqual(result.mode, "L")

    def test_convert_image_invalid_mode(self):
        img = self.sample_image.copy()
        with self.assertRaises(ValueError):
            self.processor.convert_image(img, "INVALID_MODE")

    @patch.object(Image, 'open')
    def test_process_image(self, mock_open):
        mock_open.return_value = self.sample_image
        processed_image = self.processor.process_image(BytesIO(), "Test Show")
        self.assertIsInstance(processed_image, Image.Image)  # Ensure it returns an image instance

    def test_blur(self):
        blurred_img = self.processor.blur(self.sample_image, blurFactor=5)
        self.assertEqual(blurred_img.size, self.sample_image.size)  # Ensure size remains the same

    def test_zoom(self):
        zoomed_img = self.processor.zoom(self.sample_image, zoomFactor=2)
        self.assertEqual(zoomed_img.size, (200, 200))  # Check that image is doubled in size

    def test_instagram_square_canvas(self):
        img = Image.new("RGB", (100, 50), "green")
        square_img = self.processor.instagram_square_canvas(img)
        self.assertEqual(square_img.size, (100, 100))  # Ensure it creates a square canvas

    def test_circle_mask(self):
        img = Image.new("RGBA", (100, 100), (255, 0, 0, 255))
        masked_img = self.processor.circle_mask(img, (0, 0, 255), 0.1)
        self.assertEqual(masked_img.size, img.size)  # Verify the output size matches input

    @patch('utility.draw_rounded_rectangle')
    def test_add_text(self, mock_draw_rounded_rectangle):
        font = ImageFont.load_default()
        img = self.sample_image.copy()
        result = self.processor.add_text(
            img=img, 
            text="Sample Text", 
            font=font, 
            font_ratio=0.1, 
            rectangle_color=(255, 255, 255),
            position_ratio=(0.05, 0.03),
            is_genre=False
        )
        self.assertIsInstance(result, Image.Image)  # Ensure the image is returned

    def test_overlay_image(self):
        overlay = Image.new("RGBA", (20, 20), (0, 0, 255, 128))
        result_img = self.processor.overlay_image(self.sample_image.copy(), overlay, logoRatio=0.2, offsetPercentage=(0.1, 0.1))
        self.assertIsInstance(result_img, Image.Image)  # Ensure the image is returned

    def test_replace_colors_in_image(self):
        color_map = {(0, 0, 255): (255, 0, 0)}  # Replace blue with red
        img_byte = BytesIO()
        self.sample_image.save(img_byte, format="PNG")
        img_byte.seek(0)
        modified_img = self.processor.replace_colors_in_image(img_byte, color_map)
        self.assertIsInstance(modified_img, Image.Image)  # Ensure the modified image is returned
        self.assertEqual(modified_img.getpixel((0, 0)), (255, 0, 0, 255))  # Check that color was changed

if __name__ == "__main__":
    unittest.main()
