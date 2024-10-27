
from file_handler import FileHandler
from image_processor import ImageProcessor
from dropbox.services.files import DropboxService
from datetime import datetime
from io import BytesIO
from utility import hex_to_rgb
import logging
import os
import pandas as pd

POST_SQUARE_SIZE= 1080
FONT_SHOW_SIZE_RATIO = 0.04
FONT_GENRE_SIZE_RATIO = 0.035
SHOW_TEXT = "David Barbarossa's Simple Food"
GENRE_TEXT_TEST = "Disco | Boogie | Leftfield"

class RadioBuenaVida:
    def __init__(self):
        self.dropbox_service = DropboxService()
        self.file_handler = FileHandler(self.dropbox_service)
        self.image_processor = ImageProcessor()

    def create_social_media_assets(self):
        files = self.file_handler.get_images()
        rbvBrand = self.rbv_assets()
        for file in files:
            try:
                img_data = self.file_handler.file_download(file['path_lower']) # DONE
                img = self.file_handler.open_image(img_data)
                imgBlurZoom = self.image_processor.zoom(self.image_processor.blur((img)))
                imgSquare = self.image_processor.instagram_square_canvas(img=imgBlurZoom)
                img = self.image_processor.circle_mask(img=img, borderColour=rbvBrand['rgbColor'], borderthicknessRatio=0.04)
                maskedImagePosition  = (
                    (imgSquare.width - img.width) // 2,
                    (imgSquare.height - img.height) // 2
                    ) # Calculate the position to paste the masked image (centre)
                imgSquare.paste(img, maskedImagePosition, img)
                font = self.file_handler.get_font()
                self.image_processor.add_text(
                    img=imgSquare,
                    text=SHOW_TEXT,
                    font = font,
                    font_ratio=FONT_SHOW_SIZE_RATIO,
                    rectangle_color=rbvBrand["rgbColor"],
                    is_genre=False)
                self.image_processor.add_text(
                    img=imgSquare, 
                    font = font,
                    font_ratio=FONT_GENRE_SIZE_RATIO,
                    text=GENRE_TEXT_TEST,
                    rectangle_color=rbvBrand["rgbColor"],
                    is_genre=True)
                logoFileResponse = self.dropbox_service.download_file(file_path=rbvBrand["logoFilePath"])
                rbvLogo = self.file_handler.open_image(image_data= logoFileResponse)
                rbvLogo = self.image_processor.convert_image(img=rbvLogo, convert_to="RGBA")
                imgSquare = self.image_processor.overlay_image(imgSquare, rbvLogo, 0.25, offsetPercentage=(0.05,0.075))
                websiteLogoResponse = self.dropbox_service.download_file(file_path=rbvBrand["websiteLogoFilePath"])
                rbvWebsiteLogo = self.file_handler.open_image(image_data=websiteLogoResponse)
                rbvWebsiteLogo = self.image_processor.convert_image(img=rbvWebsiteLogo,convert_to="RGBA")
                imgSquare = self.image_processor.overlay_image(imgSquare, rbvWebsiteLogo, 0.25, offsetPercentage=(0.05,0.025))
                byte_io = BytesIO()
                # Check if the image is in RGBA mode
                if imgSquare.mode == 'RGBA':
                    # Convert to RGB (removing alpha channel)
                    imgSquare = self.image_processor.convert_image(img=imgSquare, convert_to="RGBA")
                # Save the image as JPEG
                imgSquare.save(byte_io, format='JPEG')
                showName = self.rbv_file_naming(file['name'])
                self.file_handler.upload_image(img_data=byte_io.getvalue(), filename=showName)
            except Exception as e:
                print(f"Error processing file {file['name']}: {e}")
            logging.info({"statusCode": 200, "body": "Images processed and uploaded successfully"})
        return {"statusCode": 200, "body": "Images processed and uploaded successfully"}
    
    def rbv_assets(self):
        currentMonthName = datetime.now().strftime("%B")
        coloredAssetsFolder = self.dropbox_service.get_folder(folder_path=os.getenv('DROPBOX_RBV_BRAND_COLORED_ASSETS_FOLDER'))
        rbvLogoFile = [file for file in coloredAssetsFolder['entries'] if currentMonthName.lower() in file['name'].lower() and 'logo' in file['name'].lower()][0]
        rbvWebsiteLogoFile = [file for file in coloredAssetsFolder['entries'] if currentMonthName.lower() in file['name'].lower() and 'website' in file['name'].lower()][0]
        monthlyColorFile = self.dropbox_service.download_file(file_path=os.path.join(os.getenv('DROPBOX_RBV_BRAND_FOLDER'),'monthly_colors.xlsx'))
        monthlyColorsDf = pd.read_excel(BytesIO(monthlyColorFile))


        hexColor = monthlyColorsDf["Color"].loc[monthlyColorsDf["Month"]==currentMonthName].values[0]
        rbvBrand = {
            "month": currentMonthName,
            "logoFilePath":rbvLogoFile['path_lower'],
            "websiteLogoFilePath": rbvWebsiteLogoFile['path_lower'],
            "hexColor": hexColor,
            "rgbColor": hex_to_rgb(hexColor)
        }
        return rbvBrand

    def rbv_file_naming(self, showName):
        now = datetime.now()
        formattedDate = now.strftime("%d.%m")
        showFileName = f"{formattedDate} {showName}"
        return showFileName