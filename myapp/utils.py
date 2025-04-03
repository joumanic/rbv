import dropbox
from decouple import config
import os
import mimetypes
from scripts.dbx.files import DropboxService

access_token = os.getenv('DROPBOX_ACCESS_TOKEN')
dbx = DropboxService()
dbx = dbx._dbx

def upload_to_dropbox(request, file, show_name, show_date, genre1, genre2, genre3):
    # First, verify that the access token is working
    try:
        account_info = dbx.users_get_current_account()
        print("Account Info:", account_info)
    except dropbox.exceptions.AuthError as e:
        print(f"Authentication failed: {e}")
        return None

    # Determine file type
    mime_type, _ = mimetypes.guess_type(file.name)
    
    if mime_type and mime_type.startswith("audio"):  # Check if file is an audio file
        folder = "/rbv-automation/pre-records"
        extension = ".mp3"
    else:  # Default to image submissions folder
        folder = "/rbv-automation/image_submissions"
        extension = os.path.splitext(file.name)[-1]  # Preserve original image extension

    # Format date as DDMMYYYY
    formatted_date = show_date.strftime("%d%m%Y")  # Converts YYYY-MM-DD to DDMMYYYY

    # Create filename based on show details
    sanitized_show_name = show_name.replace(" ", "-").lower()
    sanitized_genres = "-".join(filter(None, [genre1, genre2, genre3])).replace(" ", "-").lower()
    filename = f"{sanitized_show_name}-{sanitized_genres}-{formatted_date}{extension}"

    # Set file path
    file_path = f"{folder}/{filename}"
    print(f"Uploading to Dropbox with file path: {file_path}")

    try:
        # Upload the file to Dropbox
        response = dbx.files_upload(file.read(), file_path, mute=True)
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings(response.path_display)
        return shared_link_metadata.url  # Return URL if successful
    except Exception as e:
        print(f"Error uploading to Dropbox: {e}")
        return None
