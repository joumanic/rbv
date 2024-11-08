import unittest
from unittest.mock import patch, MagicMock
from scripts.dropbox import DropboxService
import requests

class TestDropboxService(unittest.TestCase):

    def setUp(self):
        # Setup a DropboxService instance with a mock token
        self.dropbox_service = DropboxService(api_token="test_token")
    
    def test_missing_api_token_warning(self):
        with patch("logging.Logger.warning") as mock_warning:
            DropboxService(api_token=None)
            mock_warning.assert_called_with("Dropbox API token is missing. Set it as an environment variable or pass it explicitly.")

    def test_get_headers(self):
        headers = self.dropbox_service._get_headers(content_type="application/json")
        self.assertIn("Authorization", headers)
        self.assertEqual(headers["Authorization"], "Bearer test_token")
        self.assertEqual(headers["Content-Type"], "application/json")

    @patch("your_module.DropboxService._send_request")
    def test_batch_delete_files(self, mock_send_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "complete"}
        mock_send_request.return_value = mock_response

        response = self.dropbox_service.batch_delete_files(["/test/file1", "/test/file2"])
        self.assertEqual(response, {"status": "complete"})

    @patch("your_module.DropboxService._send_request")
    def test_get_folder(self, mock_send_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"entries": [{"name": "file1.jpg"}, {"name": "file2.png"}]}
        mock_send_request.return_value = mock_response

        response = self.dropbox_service.get_folder("/test_folder")
        self.assertEqual(response, {"entries": [{"name": "file1.jpg"}, {"name": "file2.png"}]})

    @patch("your_module.DropboxService.get_folder")
    def test_get_images(self, mock_get_folder):
        mock_get_folder.return_value = {
            "entries": [
                {"name": "file1.jpg"},
                {"name": "file2.png"},
                {"name": "document.pdf"},
            ]
        }
        images = self.dropbox_service.get_images("/test_folder")
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0]["name"], "file1.jpg")
        self.assertEqual(images[1]["name"], "file2.png")

    @patch("your_module.DropboxService._send_request")
    def test_download_file(self, mock_send_request):
        mock_response = MagicMock()
        mock_response.content = b"file_content"
        mock_send_request.return_value = mock_response

        content = self.dropbox_service.download_file("/test/file.jpg")
        self.assertEqual(content, b"file_content")

    @patch("your_module.DropboxService._send_request")
    def test_upload_file(self, mock_send_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_send_request.return_value = mock_response

        response = self.dropbox_service.upload_file("/test/file.jpg", b"file_content")
        self.assertEqual(response.status_code, 200)

    def test_get_filename_from_shareable_link(self):
        url = "https://www.dropbox.com/s/testfile.jpg?dl=0"
        filename = self.dropbox_service.get_filename_from_shareable_link(url)
        self.assertEqual(filename, "testfile.jpg")

    @patch("requests.get")
    def test_download_shareable_link(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"test content"
        mock_get.return_value = mock_response

        with patch("tempfile.NamedTemporaryFile") as mock_tempfile:
            mock_temp = MagicMock()
            mock_temp.name = "/temp/testfile"
            mock_tempfile.return_value = mock_temp

            temp_file_path = self.dropbox_service.download_shareable_link("https://www.dropbox.com/s/testfile.jpg?dl=0")
            self.assertEqual(temp_file_path, "/temp/testfile")
            mock_temp.write.assert_called_once_with(b"test content")

if __name__ == "__main__":
    unittest.main()
