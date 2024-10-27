import requests
import logging
import json
import os
from requests.exceptions import RequestException, HTTPError, Timeout, ConnectionError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DropboxService:
    def __init__(self, api_token=None):
        self.api_token = api_token or os.getenv("DROPBOX_TOKEN")
        self.base_url = "https://api.dropboxapi.com/2/files/"
        self.content_url = "https://content.dropboxapi.com/2/files/"

        if not self.api_token:
            logger.warning("Dropbox API token is missing. Set it as an environment variable or pass it explicitly.")

    def _get_headers(self, content_type="application/json", **kwargs):
        """Helper function to generate request headers."""
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": content_type
        }
        headers.update(kwargs)
        return headers

    def _send_request(self, url, method="POST", headers=None, data=None):
        """Helper function to send requests with error handling."""
        try:
            logger.info(f"Sending {method} request to {url}")
            response = requests.request(method, url, headers=headers, data=data)
            response.raise_for_status()
            logger.info("Request successful.")
            return response
        except (HTTPError, Timeout, ConnectionError, RequestException) as err:
            logger.error(f"Error occurred during request: {err}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        return None

    def get_folder(self, folder_path: str):
        """Lists contents of a Dropbox folder."""
        url = self.base_url + "list_folder"
        headers = self._get_headers()
        data = json.dumps({"path": folder_path})
        
        response = self._send_request(url, headers=headers, data=data)
        if response:
            return response.json()
        return None

    def download_file(self, file_path: str):
        """Downloads a file from Dropbox."""
        url = self.content_url + "download"
        headers = self._get_headers(content_type="application/octet-stream", **{
            "Dropbox-API-Arg": json.dumps({"path": file_path})
        })

        response = self._send_request(url, headers=headers)
        if response:
            return response.content  # Return raw file data for flexibility
        return None

    def upload_file(self, path: str, data: bytes):
        """Uploads a file to Dropbox."""
        url = self.content_url + "upload"
        headers = self._get_headers(content_type="application/octet-stream", **{
            "Dropbox-API-Arg": json.dumps({"path": path})
        })

        response = self._send_request(url, headers=headers, data=data)
        return response  # Return the entire response if needed for further inspection
