from file_handler import FileHandler
from image_processor import ImageProcessor
from asset_manager import AssetManager

class EventHandler:
    def __init__(self):
        self.file_handler = FileHandler()
        self.image_processor = ImageProcessor()
        self.asset_manager = AssetManager()
    
    def handle_event(self, event, context):
        if event.get("trigger"):
            files = self.file_handler.get_images()
            for file in files:
                try:
                    img_data = self.file_handler.file_download(file['path_lower'])
                    processed_image = self.image_processor.process_image(img_data, file['name'])
                    self.file_handler.upload_image(processed_image, file['name'])
                except Exception as e:
                    print(f"Error processing file {file['name']}: {e}")
                return {"statusCode": 200, "body": "Images processed and uploaded successfully"}
        else:
            return {"statusCode": 300, "body": "Not Triggered"} 