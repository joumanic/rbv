import dropbox
from decouple import config
import os
access_token = os.getenv('DROPBOX_ACCESS_TOKEN')
dbx = dropbox.Dropbox(access_token)

def upload_to_dropbox(request, file):
    # First, verify that the access token is working by fetching account info
    try:
        account_info = dbx.users_get_current_account()
        print("Account Info:", account_info)
    except dropbox.exceptions.AuthError as e:
        # If authentication fails, return None
        print(f"Authentication failed: {e}")
        return None

    # File path for uploading
    file_path = f'/rbv-test/{file.name}'
    print(f"Uploading to Dropbox with file path: {file_path}")

    try:
        # Upload the file to Dropbox
        response = dbx.files_upload(file.read(), file_path, mute=True)
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings(response.path_display)
        return shared_link_metadata.url  # Return URL if successful
    except Exception as e:
        # If any error occurs, print and return None
        print(f"Error uploading to Dropbox: {e}")
        return None
