import os
from dropbox.services.files import get_folder, download_file, upload_file

class FileHandler:
    def __init__(self):
        self.show_images_path = os.getenv("DROPBOX_SHOW_IMAGES")
        self.upload_path = os.getenv("DROPBOX_RBV_SHOW_IMAGES")
    
    def get_images(self):
        folder = get_folder(self.show_images_path)
        return [file for file in folder["entries"] if file["name"].lower().endswith(("png", "jpg", "jpeg"))]
    
    def file_download(self, file_path):
        return download_file(file_path = file_path).content
    
    def upload_image(self, img_data, filename):
        upload_path = os.path.join(self.upload_path, filename)
        upload_file(path=upload_path, data=img_data)
