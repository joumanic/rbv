import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import os
import pandas as pd
from io import BytesIO
from utility import hex_to_rgb
from scripts.dbx.files import DropboxService
from scripts.db.db import DatabaseHandler
from image_processor import ImageProcessor
from file_handler import FileHandler
from radio_buena_vida import RadioBuenaVida  # Assuming the main class is in this file

class TestRadioBuenaVida(unittest.TestCase):

    @patch.object(DropboxService, 'download_shareable_link')
    @patch.object(DropboxService, 'download_file')
    @patch.object(DropboxService, 'batch_delete_files')
    @patch.object(DropboxService, 'get_folder')
    @patch.object(DatabaseHandler, 'connect')
    @patch.object(DatabaseHandler, 'get_current_radio_shows')
    @patch.object(DatabaseHandler, 'close')
    @patch.object(FileHandler, 'open_image')
    @patch.object(FileHandler, 'get_font')
    @patch.object(FileHandler, 'upload_image')
    @patch.object(ImageProcessor, 'zoom')
    @patch.object(ImageProcessor, 'blur')
    @patch.object(ImageProcessor, 'instagram_square_canvas')
    @patch.object(ImageProcessor, 'circle_mask')
    @patch.object(ImageProcessor, 'add_text')
    @patch.object(ImageProcessor, 'overlay_image')
    @patch.object(ImageProcessor, 'convert_image')
    @patch.object(ImageProcessor, 'replace_colors_in_image')
    def test_create_social_media_assets(
        self, 
        mock_replace_colors, mock_convert_image, mock_overlay_image, mock_add_text, 
        mock_circle_mask, mock_instagram_square_canvas, mock_blur, mock_zoom,
        mock_upload_image, mock_get_font, mock_open_image, mock_get_current_radio_shows,
        mock_connect, mock_get_folder, mock_batch_delete_files, mock_download_file,
        mock_download_shareable_link, mock_database_handler_close
    ):
        # Setup mock data
        mock_get_current_radio_shows.return_value = pd.DataFrame([{
            "show_name": "Show 1", 
            "show_image": "path_to_image", 
            "genre_1": "Pop", "genre_2": "Rock", "genre_3": "",
        }])

        mock_download_shareable_link.return_value = b"image_data"
        mock_open_image.return_value = MagicMock()
        mock_get_font.return_value = MagicMock()
        mock_zoom.return_value = MagicMock()
        mock_blur.return_value = MagicMock()
        mock_instagram_square_canvas.return_value = MagicMock(width=1080, height=1080)
        mock_circle_mask.return_value = MagicMock()
        mock_add_text.return_value = None
        mock_overlay_image.return_value = MagicMock()
        mock_convert_image.return_value = MagicMock()
        mock_replace_colors.return_value = MagicMock()
        mock_upload_image.return_value = None
        mock_download_file.return_value = b"logo_data"

        # Create instance of RadioBuenaVida
        radio_buena_vida = RadioBuenaVida()

        # Call the method
        radio_buena_vida.create_social_media_assets()

        # Assertions
        mock_connect.assert_called_once()
        mock_get_current_radio_shows.assert_called_once()
        mock_open_image.assert_called_once_with(image_data=b"image_data")
        mock_zoom.assert_called_once()
        mock_blur.assert_called_once()
        mock_instagram_square_canvas.assert_called_once()
        mock_circle_mask.assert_called_once()
        mock_add_text.assert_called()
        mock_overlay_image.assert_called()
        mock_upload_image.assert_called()
        mock_batch_delete_files.assert_called()

    @patch.object(DropboxService, 'download_file')
    @patch.object(DropboxService, 'get_folder')
    def test_create_monthly_colors_assets(self, mock_get_folder, mock_download_file):
        # Setup mock data
        mock_download_file.return_value = b"monthly_colors_data"
        mock_get_folder.return_value = MagicMock(entries=[MagicMock(path_lower='template_path')])

        monthly_color_df = pd.DataFrame({
            "Month": ["January", "February"],
            "Color": ["#FFFFFF", "#000000"]
        })
        mock_download_file.return_value = monthly_color_df.to_excel()

        radio_buena_vida = RadioBuenaVida()

        # Call the method
        radio_buena_vida.create_monthly_colors_assets()

        # Assertions
        mock_download_file.assert_called()
        mock_get_folder.assert_called()

    @patch.object(DropboxService, 'get_folder')
    @patch.object(DropboxService, 'download_file')
    def test_rbv_assets(self, mock_download_file, mock_get_folder):
        # Setup mock data
        mock_download_file.return_value = b"brand_data"
        mock_get_folder.return_value = MagicMock(entries=[MagicMock(path_lower="logo_path")])

        radio_buena_vida = RadioBuenaVida()

        # Call the method
        rbv_assets = radio_buena_vida.rbv_assets()

        # Assertions
        self.assertIn("logoFilePath", rbv_assets)
        self.assertIn("websiteLogoFilePath", rbv_assets)
        self.assertIn("hexColor", rbv_assets)

    def test_rbv_file_naming(self):
        radio_buena_vida = RadioBuenaVida()

        # Call the method
        file_name = radio_buena_vida.rbv_file_naming("Test Show")

        # Assertions
        current_date = datetime.now().strftime("%d.%m")
        self.assertTrue(file_name.startswith(current_date))
        self.assertTrue("Test Show" in file_name)

if __name__ == "__main__":
    unittest.main()
