from PIL import Image, ImageDraw, ImageFont
from asset_manager import AssetManager
from utility import draw_rounded_rectangle

class ImageProcessor:
    def __init__(self):
        self.asset_manager = AssetManager()
    
    def process_image(self, image_data, show_name):
        img = Image.open(image_data)
        processed_image = self.apply_transformations(img)
        self.add_text(processed_image, show_name)
        return processed_image
    
    def apply_transformations(self, img):
        # Transform image by blurring, zooming, masking
        return img
    
    def add_text(self, img, show_name):
        draw = ImageDraw.Draw(img)
        font = self.asset_manager.get_font()
        draw.text((10,10), show_name, font = font, fill="black")