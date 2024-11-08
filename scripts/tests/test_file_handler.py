import unittest
from unittest.mock import MagicMock, patch
from io import BytesIO
from PIL import Image
from scripts.file_handler import FileHandler

class TestFileHandler(unittest.TestCase):

    def setUp(self):
        # Mock the dropbox_service dependency
        self.dropbox_service_mock = MagicMock()
        self.file_handler = FileHandler(dropbox_service=self.dropbox_service_mock)

    def test_file_download_success(self):
        # Mock successful file download
        self.dropbox_service_mock.download_file.return_value = b"file_content"
        
        result = self.file_handler.file_download("test_path/file.txt")
        self.assertEqual(result, b"file_content")
        self.dropbox_service_mock.download_file.assert_called_once_with("test_path/file.txt")

    def test_file_download_failure(self):
        # Mock failed file download
        self.dropbox_service_mock.download_file.return_value = None
        
        result = self.file_handler.file_download("test_path/nonexistent.txt")
        self.assertIsNone(result)
        self.dropbox_service_mock.download_file.assert_called_once_with("test_path/nonexistent.txt")

    def test_upload_image_success(self):
        # Mock successful upload
        self.dropbox_service_mock.upload_file.return_value = True
        
        with patch("builtins.print") as mock_print:
            self.file_handler.upload_image(b"image_data", "test_image.jpg", "/test/path")
            self.dropbox_service_mock.upload_file.assert_called_once_with(path="/test/path/test_image.jpg", data=b"image_data")
            mock_print.assert_called_once_with("File uploaded successfully.")

    def test_upload_image_failure(self):
        # Mock failed upload
        self.dropbox_service_mock.upload_file.return_value = False
        
        with patch("builtins.print") as mock_print:
            self.file_handler.upload_image(b"image_data", "test_image.jpg", "/test/path")
            self.dropbox_service_mock.upload_file.assert_called_once_with(path="/test/path/test_image.jpg", data=b"image_data")
            mock_print.assert_called_once_with("Failed to upload the file.")

    def test_open_image_success(self):
        # Test opening a valid image file
        img = Image.new("RGB", (100, 100), color="blue")
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format="PNG")
        img_data = img_byte_arr.getvalue()
        
        with patch("logging.info") as mock_logging:
            result = self.file_handler.open_image(img_data)
            self.assertIsInstance(result, Image.Image)
            mock_logging.assert_called_once_with("Image opened successfully.")

    def test_open_image_failure(self):
        # Test opening invalid image data (should log an error)
        with patch("logging.error") as mock_logging:
            result = self.file_handler.open_image(b"not an image")
            self.assertIsNone(result)
            mock_logging.assert_called_once()

    @patch("os.getenv")
    def test_get_font_success(self, mock_getenv):
        # Mocking the environment variable and a successful font download
        mock_getenv.return_value = "/mock/path"
        self.dropbox_service_mock.download_file.return_value = b"font_data"
        
        font_data = self.file_handler.get_font()
        self.assertIsInstance(font_data, BytesIO)
        self.dropbox_service_mock.download_file.assert_called_once_with("/mock/path/din2014_demi.otf")

    @patch("os.getenv")
    def test_get_font_failure(self, mock_getenv):
        # Mocking the environment variable and a failed font download
        mock_getenv.return_value = "/mock/path"
        self.dropbox_service_mock.download_file.side_effect = IOError("Download failed")

        with patch("logging.error") as mock_logging:
            font_data = self.file_handler.get_font()
            self.assertIsNone(font_data)
            mock_logging.assert_called_once_with("Failed to load custom font 'din2014_demi.otf': Download failed")

if __name__ == "__main__":
    unittest.main()
