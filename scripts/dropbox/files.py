import requests
import logging
import json
import os
import tempfile
from requests.exceptions import RequestException, HTTPError, Timeout, ConnectionError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DropboxService:
    def __init__(self, api_token=None):
        self.api_token = os.getenv("DROPBOX_ACCESS_TOKEN")
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
    
    def get_images(self, folder_path:str):
        folder = self.get_folder(folder_path)
        if folder and "entries" in folder:
            return [file for file in folder["entries"] if file["name"].lower().endswith(("png", "jpg", "jpeg"))]
        return []
    
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

    def download_shareable_link(self, link:str):
        try:
            # Modify the link to ensure it downloads the file
            modified_link = link.replace("dl=0", "dl=1")
            logging.info(f"Modified link for download: {modified_link}")

            # Send a GET request to the modified link
            response = requests.get(modified_link)

            # Check if the request was successful
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    # Write the content to the temporary file
                    temp_file.write(response.content)
                    logging.info("File downloaded successfully!")
                    temp_file_path = temp_file.name  # Get the name of the temporary file
                    return temp_file_path  # Return the path of the temporary file
            else:
                logging.error(f"Failed to download file. Status code: {response.status_code}")
                return None  # Return None if the download fails

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            return None  # Return None if a request exception occurs

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return None  # Return None if an unexpected error occurs