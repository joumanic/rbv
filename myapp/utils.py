import dropbox
from django.conf import settings

def upload_to_dropbox(file):
    dbx = dropbox.Dropbox(settings.DROPBOX_ACCESS_TOKEN)
    file_path = f'/image_submissions/{file.name}'
    try:
        upload_result = dbx.files_upload(file.read(), file_path, mute=True)
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings(file_path)
        return shared_link_metadata.url
    except Exception as e:
        print(f'Error uploading to Dropbox: {e}')
        return None