import os
from io import BytesIO
import logging
from PIL import Image

class FileHandler:
    def __init__(self, dropbox_service):
        self.dropbox_service = dropbox_service  
    
    def file_download(self, file_path):
        response_content = self.dropbox_service.download_file(file_path)
        if response_content:
            return response_content  # Return the raw file content
        return None
        
    def upload_image(self, img_data, filename, path):
        upload_path = os.path.join(path, filename)
        response = self.dropbox_service.upload_file(path=upload_path, data=img_data)
        if response:
            print("File uploaded successfully.")
        else:
            print("Failed to upload the file.")

    def open_image(self, image_data):
        try:
            # Check if image_data is in bytes format or wrap it as BytesIO
            if isinstance(image_data, bytes):
                image_data = BytesIO(image_data)

            # Try opening the image
            image = Image.open(image_data)
            logging.info("Image opened successfully.")
            return image

        except IOError as e:
            logging.error(f"Failed to open image: {e}")
            return None
        