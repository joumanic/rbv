import os
from dropbox.services.files import DropboxService

class FileHandler:
    def __init__(self):
        self.show_images_path = os.getenv("DROPBOX_SHOW_IMAGES")
        self.upload_path = os.getenv("DROPBOX_RBV_SHOW_IMAGES")
        self.dropbox_service = DropboxService()  # Initialize DropboxService
    
    def get_images(self):
        folder = self.dropbox_service.get_folder(self.show_images_path)
        if folder and "entries" in folder:
            return [file for file in folder["entries"] if file["name"].lower().endswith(("png", "jpg", "jpeg"))]
        return []
    
    def file_download(self, file_path):
        response_content = self.dropbox_service.download_file(file_path)
        if response_content:
            return response_content  # Return the raw file content
        return None
        
    def upload_image(self, img_data, filename):
        upload_path = os.path.join(self.upload_path, filename)
        response = self.dropbox_service.upload_file(path=upload_path, data=img_data)
        if response:
            print("File uploaded successfully.")
        else:
            print("Failed to upload the file.")
