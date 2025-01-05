import requests
import logging
import os
import tempfile
from urllib.parse import urlparse, unquote
import dropbox
from dropbox.exceptions import ApiError, AuthError
from dropbox.oauth import OAuth2FlowNoRedirectResult
from dropbox.files import DeleteArg as DropboxDeleteArg
from dropbox.files import UploadError, WriteError, WriteConflictError, UploadWriteFailed
from decouple import config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DropboxService:
    def __init__(self):
        self._sdk_token = config("DROPBOX_ACCESS_TOKEN")
        self._initialize_client()
        if not self._sdk_token:
            logging.warning("Dropbox SDK access token is missing. Set it as an environment variable.")

    def _initialize_client(self):
        """Initialize Dropbox client."""
        #TODO: make better logic to refresh token only when necessary
        try:
            self._sdk_token = self._refresh_token()
            self._dbx = dropbox.Dropbox(self._sdk_token)
        except AuthError:
            logging.warning("Initial authentication failed. Attempting to refresh token.")
            self._sdk_token = self._refresh_token()
            self._dbx = dropbox.Dropbox(self._sdk_token)

    def _refresh_token(self):
        refresh_token = os.getenv('DROPBOX_REFRESH_TOKEN')
        app_key = os.getenv('DROPBOX_APP_KEY')
        app_secret = os.getenv('DROPBOX_APP_SECRET')
        
        url = "https://api.dropboxapi.com/oauth2/token"
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': app_key,
            'client_secret': app_secret
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            new_access_token = response.json()['access_token']
            # Save this token securely (e.g., in an environment variable or secure store)
            os.environ['DROPBOX_ACCESS_TOKEN'] = new_access_token
            return new_access_token
        else:
            raise Exception("Failed to refresh access token: {}".format(response.json()))
    def _retry_on_auth_error(self, func, *args, **kwargs):
        """Retry a Dropbox SDK operation if AuthError occurs."""
        try:
            return func(*args, **kwargs)
        except AuthError as e:
            logging.warning(f"AuthError encountered: {e}. Attempting to refresh token and retry.")
            self._sdk_token = self._refresh_token()
            self._dbx = dropbox.Dropbox(self._sdk_token)
            return func(*args, **kwargs)  # Retry operation after refreshing token


    def batch_delete_files(self, file_paths:list):
        """Batch delete files"""
        entries = [DropboxDeleteArg(path) for path in file_paths]
        self._retry_on_auth_error(self._dbx.files_delete_batch, entries=entries)


    def get_folder(self, folder_path: str):
        """Lists contents of a Dropbox folder."""
        return self._retry_on_auth_error(self._dbx.files_list_folder, path=folder_path)
    
    def get_images(self, folder_path:str):
        listFolder = self.get_folder(folder_path)
        if listFolder.entries:
            return [file for file in listFolder.entries if file.name.lower().endswith(("png", "jpg", "jpeg"))]
        return []
    
    def download_file(self, file_path: str):
        """Downloads a file from Dropbox."""
        _,response =  self._retry_on_auth_error(self._dbx.files_download, file_path)
        if response.status_code == 200:
            return response.content  # Return raw file data for flexibility
        return None

    def upload_file(self, path: str, data: bytes):
        """Uploads a file to Dropbox, handling conflicts by appending a suffix."""
        original_path = path
        attempt = 0

        while True:
            try:
                # Try uploading the file
                return self._retry_on_auth_error(self._dbx.files_upload, data, path)
            except ApiError as e:
                # Check if the error is an UploadError with a path conflict
                if isinstance(e.error, UploadError):
                    upload_failed = e.error.get_path()
                    if isinstance(upload_failed, WriteError) or isinstance(upload_failed, UploadWriteFailed):
                        if isinstance(upload_failed.reason, WriteConflictError) or isinstance(upload_failed.reason, WriteError):
                            # Increment the suffix and modify the path
                            attempt += 1
                            base, ext = os.path.splitext(original_path)
                            path = f"{base}-{attempt}{ext}"
                            logging.warning(f"File conflict detected. Retrying with new name: {path}")
                            continue
                # If it's a different error, re-raise
                logging.error(f"Unhandled error during upload: {e}")

    def get_filename_from_shareable_link(self, url:str) -> str:
        """Gets filename from shareable link"""
        parsed_url = urlparse(url)
        
        # Extract the last part of the path (the filename)
        filename = parsed_url.path.split('/')[-1]
        
        # Decode any URL-encoded characters
        return unquote(filename)

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