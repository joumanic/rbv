import unittest
from unittest.mock import patch, Mock, call
from datetime import datetime
from io import BytesIO
from scripts.brand import RadioBuenaVida  

class TestRadioBuenaVida(unittest.TestCase):
    
    @patch('your_module.DatabaseHandler')
    @patch('your_module.DropboxService')
    @patch('your_module.FileHandler')
    @patch('your_module.ImageProcessor')
    def setUp(self, MockImageProcessor, MockFileHandler, MockDropboxService, MockDatabaseHandler):
        # Mock dependencies
        self.mock_database_handler = MockDatabaseHandler.return_value
        self.mock_dropbox_service = MockDropboxService.return_value
        self.mock_file_handler = MockFileHandler.return_value
        self.mock_image_processor = MockImageProcessor.return_value

        # Instantiate the class with mocked dependencies
        self.rbv = RadioBuenaVida()
        
    def test_create_social_media_assets(self):
        # Mock data for database and other interactions
        self.mock_database_handler.get_current_radio_shows.return_value = pd.DataFrame([{
            "show_name": "Morning Jazz",
            "show_image": "mock_link",
            "genre_1": "Jazz",
            "genre_2": "Soul",
            "genre_3": "Blues"
        }])
        
        # Mock return values for methods used in create_social_media_assets
        self.mock_dropbox_service.download_shareable_link.return_value = b"image_data"
        self.mock_file_handler.open_image.return_value = Mock()
        self.mock_image_processor.blur.return_value = Mock()
        self.mock_image_processor.zoom.return_value = Mock()
        self.mock_image_processor.instagram_square_canvas.return_value = Mock()
        self.mock_image_processor.circle_mask.return_value = Mock()
        self.mock_file_handler.get_font.return_value = Mock()
        self.mock_dropbox_service.download_file.return_value = b"logo_data"
        
        # Call the method
        self.rbv.create_social_media_assets()
        
        # Verify method calls
        self.mock_database_handler.connect.assert_called_once()
        self.mock_database_handler.get_current_radio_shows.assert_called_once()
        self.mock_dropbox_service.download_shareable_link.assert_called_once()
        self.mock_file_handler.open_image.assert_called_once()
        self.mock_image_processor.blur.assert_called_once()
        self.mock_image_processor.zoom.assert_called_once()
        self.mock_image_processor.instagram_square_canvas.assert_called_once()
        self.mock_image_processor.circle_mask.assert_called_once()
        self.mock_dropbox_service.download_file.assert_called()
        self.mock_database_handler.close.assert_called_once()
        self.mock_dropbox_service.batch_delete_files.assert_called_once()

    def test_create_monthly_colors_assets(self):
        # Mock data for monthly colors
        monthly_colors_data = pd.DataFrame({
            "Month": ["January", "February"],
            "Color": ["#FFFFFF", "#000000"]
        })
        
        # Set up mocks
        self.mock_dropbox_service.download_file.return_value = BytesIO(b"file_data")
        with patch('pandas.read_excel', return_value=monthly_colors_data):
            self.rbv.create_monthly_colors_assets()
        
        # Verify calls
        self.mock_dropbox_service.download_file.assert_called_once()
        self.mock_dropbox_service.get_folder.assert_called_once()
        self.mock_dropbox_service.upload_file.assert_called()

    def test_rbv_assets(self):
        # Mock folder data for assets
        self.mock_dropbox_service.get_folder.return_value = {
            'entries': [
                {'name': 'january_logo.png', 'path_lower': '/mock/path/logo'},
                {'name': 'january_website_logo.png', 'path_lower': '/mock/path/website_logo'}
            ]
        }
        monthly_colors_data = pd.DataFrame({
            "Month": ["January"],
            "Color": ["#FFFFFF"]
        })

        # Set up mocks
        self.mock_dropbox_service.download_file.return_value = BytesIO(b"file_data")
        with patch('pandas.read_excel', return_value=monthly_colors_data):
            rbv_brand = self.rbv.rbv_assets()
        
        # Assertions
        self.assertEqual(rbv_brand["month"], datetime.now().strftime("%B"))
        self.assertEqual(rbv_brand["logoFilePath"], '/mock/path/logo')
        self.assertEqual(rbv_brand["websiteLogoFilePath"], '/mock/path/website_logo')
        self.assertEqual(rbv_brand["hexColor"], "#FFFFFF")

    def test_rbv_file_naming(self):
        # Test file naming
        show_name = "Jazz Show"
        expected_name = f"{datetime.now().strftime('%d.%m')} Jazz Show"
        result = self.rbv.rbv_file_naming(show_name)
        self.assertEqual(result, expected_name)

    def test_create_social_media_assets_handles_exception(self):
        # Test error handling in create_social_media_assets
        self.mock_database_handler.get_current_radio_shows.return_value = pd.DataFrame([{
            "show_name": "Error Show",
            "show_image": "error_link"
        }])
        
        # Force an exception in file handling to test error handling
        self.mock_file_handler.open_image.side_effect = Exception("Mocked exception")
        
        # Call the method
        with self.assertLogs(level="INFO") as log:
            self.rbv.create_social_media_assets()
        
        # Check that the error log was created
        self.assertIn("Error processing file Error Show", log.output[0])

if __name__ == "__main__":
    unittest.main()
