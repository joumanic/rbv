from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.conf import settings
import dropbox

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

def handle_upload(request):
    if request.method == 'POST' and request.FILES.get('show_image'):
        show_image = request.FILES['show_image']
        
        # Upload the file to Dropbox and get the URL
        dropbox_url = upload_to_dropbox(show_image)        
        if dropbox_url:
            return JsonResponse({"status": "success", "url": dropbox_url})
        else:
            return JsonResponse({"status": "error", "message": "Failed to upload to Dropbox"})
    
    return JsonResponse({"status": "error", "message": "No file uploaded"})
