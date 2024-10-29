import os
from io import BytesIO
import logging
from PIL import Image

class FileHandler:
    def __init__(self, dropbox_service):
        self.show_images_path = os.getenv("DROPBOX_SHOW_IMAGES")
        self.upload_path = os.getenv("DROPBOX_RBV_SHOW_IMAGES")
        self.dropbox_service = dropbox_service  
    
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

    def open_image(self, image_data):
        try:
            # Check if image_data is in bytes format or wrap it as BytesIO
            if isinstance(image_data, bytes):
                image_data = BytesIO(image_data)
            elif not isinstance(image_data, BytesIO):
                logging.error("Invalid image data format: must be bytes or BytesIO.")
                return None

            # Try opening the image
            image = Image.open(image_data)
            logging.info("Image opened successfully.")
            return image

        except IOError as e:
            logging.error(f"Failed to open image: {e}")
            return None
        
    def get_font(self, font_file_name='din2014_demi.otf', font_size_ratio=0.05):
        # Load and return font file for the current month
        try:
            fontFile = self.dropbox_service.download_file(file_path=os.path.join(os.getenv('DROPBOX_RBV_BRAND_FOLDER'),'din2014_demi.otf'))
            font = BytesIO(fontFile)
            return font
        except IOError as e:
            logging.error(f"Failed to load custom font '{font_file_name}': {e}")

