from file_handler import FileHandler
from scripts.dbx.files import DropboxService
from scripts.db.db import DatabaseHandler
from datetime import datetime
import image_processor
from dateutil.relativedelta import relativedelta
from io import BytesIO
from utility import hex_to_rgb
import logging
import os
import pandas as pd

# Dictionary to map month names to month numbers
MONTH_NAME_TO_NUMBER = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}

class RadioBuenaVida:
    def __init__(self):
        self.dropbox_service = DropboxService()
        self.file_handler = FileHandler(self.dropbox_service)
        self.database_handler = DatabaseHandler()

    def create_show_social_media_assets(self):
        self.database_handler.connect()
        radio_shows = self.database_handler.get_current_radio_shows()
        rbvBrand = self.rbv_assets()
        delete_files = []
        for _, show in radio_shows.iterrows():
            try:
                if rbvBrand['month'] != show["show_date"].strftime("%B"):
                    rbvBrand = self.rbv_assets(show["show_date"])

                img = self.file_handler.open_image(image_data=(self.dropbox_service.download_shareable_link(show["show_image"])))

                imgBlurZoom = image_processor.zoom(image_processor.blur(img, blurFactor=3))

                imgSquare = image_processor.square_image(img=imgBlurZoom)

                img = image_processor.circle_mask(img=img, borderColour=rbvBrand['rgbColor'], borderthicknessRatio=0.08)

                maskedImagePosition  = (
                    (imgSquare.width - img.width) // 2,
                    (imgSquare.height - img.height) // 2
                    ) # Calculate the position to paste the masked image (centre)
                
                imgSquare.paste(img, maskedImagePosition, img)

                logoFileResponse = self.dropbox_service.download_file(file_path=rbvBrand["logoFilePath"])

                rbvLogo = self.file_handler.open_image(image_data= logoFileResponse)

                rbvLogo = image_processor.convert_image(img=rbvLogo, convert_to="RGBA")

                imgSquare = image_processor.overlay_image(imgSquare, rbvLogo, 0.25, offsetPercentage=(0.02,0.080))

                websiteLogoResponse = self.dropbox_service.download_file(file_path=rbvBrand["websiteLogoFilePath"])

                rbvWebsiteLogo = self.file_handler.open_image(image_data=websiteLogoResponse)

                rbvWebsiteLogo = image_processor.convert_image(img=rbvWebsiteLogo,convert_to="RGBA")

                imgSquare = image_processor.overlay_image(imgSquare, rbvWebsiteLogo, 0.3, offsetPercentage=(0.02,0.025))

                rbvImg = image_processor.resize_to_square_canvas(img=imgSquare)

                genres = " | ".join([show[f"genre{i}"] for i in range(1, 4) if show.get(f"genre{i}")])

                font = self.dropbox_service.download_file(file_path=os.path.join(os.getenv('DROPBOX_RBV_BRAND_FOLDER'),'din2014_demi.otf'))
                font = BytesIO(font) # Convert to BytesIO object to be used by PIL
                image_processor.add_text(
                    img=rbvImg,
                    text=show["show_name"],
                    font = font,
                    rectangle_color=rbvBrand["rgbColor"],
                    is_genre=False)
                
                font = self.dropbox_service.download_file(file_path=os.path.join(os.getenv('DROPBOX_RBV_BRAND_FOLDER'),'din2014_demi.otf'))
                font = BytesIO(font) # Convert to BytesIO object to be used by PIL
                image_processor.add_text(
                    img=rbvImg, 
                    font = font,
                    text=genres,
                    rectangle_color=rbvBrand["rgbColor"],
                    is_genre=True)
                
                byte_io = BytesIO()
                # Check if the image is in RGBA mode
                if rbvImg.mode == 'RGBA':
                    # Convert to RGB (removing alpha channel)
                    rbvImg = image_processor.convert_image(img=rbvImg, convert_to="RGBA")
                
                # Save the image as JPEG
                rbvImg.save(byte_io, format='JPEG')

                showName = self.rbv_file_naming(f"{show['show_name']}.jpg", show["show_date"])

                # Upload the image to Dropbox
                upload_path = os.path.join(os.getenv("DROPBOX_RBV_SHOW_IMAGES"), showName)
                self.dropbox_service.upload_file(path=upload_path, data=byte_io.getvalue())

                # Delete files after processing
                file_name = self.dropbox_service.get_filename_from_shareable_link(show["show_image"])
                file_path = os.getenv("DROPBOX_SHOW_IMAGES")
                delete_files.append(os.path.join(file_path, file_name))

            except Exception as e:
                logging.info("Error processing file %s: %s",show['show_name'],e)
                
        self.database_handler.close()
        #self.dropbox_service.batch_delete_files(file_paths=delete_files)
        logging.info({"statusCode": 200, "body": "Images processed and uploaded successfully"})
    
    def create_monthly_colors_assets(self):
        monthlyColorByteFile = self.dropbox_service.download_file(file_path=os.path.join(os.getenv('DROPBOX_RBV_BRAND_FOLDER'),'monthly_colors.xlsx'))
        monthlyColorsDf = pd.read_excel(BytesIO(monthlyColorByteFile))
        
        current_date = datetime.now()
        current_month = current_date.strftime("%B")  # Get current month in abbreviated form
        next_month_start = current_date + relativedelta(months=1)
        next_month_start = next_month_start.strftime("%B")

        # Get assets for the current month
        current_month_assets = monthlyColorsDf[monthlyColorsDf["Month"] == current_month]

        # Get assets for the next month if next week crosses into it
        next_month_assets = monthlyColorsDf[monthlyColorsDf["Month"] == next_month_start]
        # Combine both DataFrames if needed
        currentMonthColor = pd.concat([current_month_assets, next_month_assets]).reset_index(drop=True)

        # Display the resulting DataFrame
        try:
            for _,row in currentMonthColor.iterrows():
                month = row["Month"]
                monthNumber = MONTH_NAME_TO_NUMBER.get(month.replace(" ",""))
                hexColor = row['Color']
                monthlyColor = hex_to_rgb(hexColor)

                brandTemplateFolder = self.dropbox_service.get_folder(os.getenv('DROPBOX_RBV_BRAND_TEMPLATES_FOLDER'))

                brandTemplates = [file for file in brandTemplateFolder.entries]
                try:
                    for file in brandTemplates:
                        fileName = f"{monthNumber}_{month}_{file.name}"
                        fileDownlaodResponse = self.dropbox_service.download_file(file_path=file.path_lower)
                        logo = self.file_handler.open_image(fileDownlaodResponse)
                        logo = image_processor.convert_image(img=logo, convert_to="RGBA")
                        fileByte = BytesIO(fileDownlaodResponse)
                        color_replacement = {
                            (255, 255, 255): monthlyColor
                        }
                        logo = image_processor.replace_colors_in_image(img_byte=fileByte, color_map=color_replacement)
                        byte_io = BytesIO()
                        if logo.mode == 'CMYK':
                            # Convert to RGB (removing alpha channel)
                            logo = image_processor.convert_image(img=logo, convert_to="RGBA")
                            logo.save(byte_io, format='JPEG')
                        else:
                            logo.save(byte_io, "PNG")
                        self.dropbox_service.upload_file(path= os.path.join(os.getenv('DROPBOX_RBV_BRAND_COLORED_ASSETS_FOLDER'),fileName), data=byte_io.getvalue())
                        logging.info({"statusCode": 200, "body": f"Asset {fileName} created and uploaded successfully"})
                except Exception as e:
                    logging.info(f"Error creating {fileName} monthly color assets: {e}")
        except Exception as e:
                logging.info(f"Error gettting monthly color template assets: {e}")

    def rbv_assets(self, showDate=datetime.now()):
        currentMonthName = showDate.strftime("%B")
        coloredAssetsFolder = self.dropbox_service.get_folder(folder_path=os.getenv('DROPBOX_RBV_BRAND_COLORED_ASSETS_FOLDER'))
        rbvLogoFile = [file for file in coloredAssetsFolder.entries if currentMonthName.lower() in file.name.lower() and 'logo' in file.name.lower()][0]
        rbvWebsiteLogoFile = [file for file in coloredAssetsFolder.entries if currentMonthName.lower() in file.name.lower() and 'website' in file.name.lower()][0]
        monthlyColorFile = self.dropbox_service.download_file(file_path=os.path.join(os.getenv('DROPBOX_RBV_BRAND_FOLDER'),'monthly_colors.xlsx'))
        monthlyColorsDf = pd.read_excel(BytesIO(monthlyColorFile))


        hexColor = monthlyColorsDf["Color"].loc[monthlyColorsDf["Month"]==currentMonthName].values[0]
        rbvBrand = {
            "month": currentMonthName,
            "logoFilePath":rbvLogoFile.path_lower,
            "websiteLogoFilePath": rbvWebsiteLogoFile.path_lower,
            "hexColor": hexColor,
            "rgbColor": hex_to_rgb(hexColor)
        }
        return rbvBrand

    def rbv_file_naming(self, showName, showDate):
        formattedDate = showDate.strftime("%d.%m.%y")
        showName = showName.replace('/', '')
        showFileName = f"{formattedDate} {showName}"
        return showFileName

