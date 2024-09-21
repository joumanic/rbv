'''
Description:

'''
from io import BytesIO
import os 
from PIL import Image
import pandas as pd
from dropbox.services.files import get_folder,download_file, upload_file

# Temporary paths while we integrate in Dropbox
RBV_BRAND_FOLDER = "scripts/data/rbv_brand"
MONTHLY_COLORS = "scripts/data/monthly_colors/monthly_colors.xlsx"
OUTPUT_FOLDER = "scripts/data/rbv_monthly_colors"
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


def logic_handler():
    # TODO look for folder with blank assets
    # Load and replace white color to monthly color for Radio Buena Vida Logo
    monthlyColorFile = download_file(filePath=os.path.join(os.getenv('DROPBOX_RBV_BRAND_BRAND_FOLDER'),'monthly_colors.xlsx'))
    monthlyColorsDf = pd.read_excel(BytesIO(monthlyColorFile.content))
    for index, row in monthlyColorsDf.iterrows():
        monthName = row['Month']
        monthNumber = MONTH_NAME_TO_NUMBER.get(monthName.replace(" ",""))
        hexColor = row['Color']
        monthlyColor = hex_to_rgb(hexColor)

        brandTemplateFolder = get_folder(os.getenv('DROPBOX_RBV_BRAND_TEMPLATES_FOLDER'))

        brandTemplates = [file for file in brandTemplateFolder['entries']]
        
        for file in brandTemplates:
            fileDownlaodResponse = download_file(filePath=file['path_lower'])
            fileByte = BytesIO(fileDownlaodResponse.content)
            with Image.open(fileByte) as logo:
                logo = logo.convert("RGBA")
                data = logo.getdata()
                new_data = [
                    (monthlyColor[0], monthlyColor[1], monthlyColor[2], item[3]) if item[:3] == (255, 255, 255) else item
                    for item in data
                ]
                logo.putdata(new_data)
                byte_io = BytesIO()
                logo.save(byte_io, format='PNG')

                upload_file(path= os.path.join(os.getenv('DROPBOX_RBV_BRAND_BRAND_FOLDER'),f"{monthNumber}_{monthName}_{file['name']}"), data=byte_io.getvalue())
                

    # TODO process assets to Monthly Colors file specifications
    # TODO upload assets to Dropbox
    # TODO if somethin in the Monthly Colors file changes then change colors 

    return 'RBV asset images processed and uploaded succesfully'


def hex_to_rgb(hex_color):
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


if __name__ == "__main__":
    logic_handler()