from PIL import Image, ImageDraw, ImageFont, ImageFilter
from utility import draw_rounded_rectangle
import logging
from io import BytesIO

class ImageProcessor:
    def __init__(self):
        pass

    def convert_image(self,img, convert_to):
        try:
            img.convert(convert_to)
            return img
        except ValueError as e:
            raise ValueError(f"Invalid conversion mode: {convert_to}. Valid modes are: {self.VALID_MODES}")

    def process_image(self, image_data, show_name):
        img = Image.open(BytesIO(image_data))
        processed_image = self.apply_transformations(img)
        self.add_text(processed_image, show_name, )
        return processed_image
    
    def apply_transformations(self, img):
        # Transform image by blurring, zooming, masking
        return img

    def blur(self, img, blurFactor: float = 15):
        imgBlurred = img.filter(ImageFilter.GaussianBlur(blurFactor))
        return imgBlurred

    def zoom(self, img, zoomFactor: float = 1.5) -> Image:
        imgZoomed = img.resize(
            (int(img.width * zoomFactor), int(img.height * zoomFactor)),
            resample=Image.LANCZOS
        )
        return imgZoomed

    def instagram_square_canvas(self, img: Image):
        size = min(img.width, img.height)
        imgSquare = Image.new("RGB", (size, size))
        offset = ((size - img.width) // 2, (size - img.height) // 2)
        imgSquare.paste(img, offset)
        return imgSquare

    def circle_mask(self, img: Image, borderColour: tuple, borderthicknessRatio: float = 0.04) -> Image:
        """
        Masks an image (`img`) to fit within a circular shape with a specified border.
        """
        # Calculate the diamter of the circle
        diameter = min(img.size[0], img.size[1]) * 0.95
        
        # Create a circular mask based on the image size
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)

        # Calculate bounding box for the circle mask
        bbox = (
            (img.size[0] - diameter) // 2, 
            (img.size[1] - diameter) // 2,
            (img.size[0] + diameter) // 2,
            (img.size[1] + diameter) // 2
        )

        # Draw the outer circle for masking
        draw.ellipse(bbox, fill=255)

        # Create a new image for the masked result
        maskedImage = Image.new("RGBA", img.size, (0, 0, 0, 0))
        maskedImage.paste(img, (0,0), mask)

        # Calculate the border thickness as a fraction of the diameter
        borderThickness = int(diameter * borderthicknessRatio)

        # If border thickness is specified, draw a border around the circle
        if borderThickness > 0:
            borderColour = borderColour + (255,) # Add alpha channel (fully opaque)

            # Create a new image for the border
            borderImage = Image.new("RGBA", img.size, (0, 0, 0, 0))
            drawBorder = ImageDraw.Draw(borderImage)

            # Draw the outer border
            outerBbox = (
                (bbox[0]) - borderThickness // 2,
                (bbox[1]) - borderThickness // 2,
                (bbox[2]) + borderThickness // 2,
                (bbox[3]) + borderThickness // 2
            )
            drawBorder.ellipse(outerBbox, outline=borderColour, width=borderThickness)

            # Composite the masked image onto the border image
            borderImage.paste(im=img, box=(0,0), mask=maskedImage)
            return borderImage
        else:
            return maskedImage
        
    def add_text(self, img, text, font, font_ratio, rectangle_color, position_ratio=(0.05, 0.03), is_genre=False):
        image_width, image_height = img.size
        draw = ImageDraw.Draw(img)

        # Modify font for the text
        font_size = int(image_height * font_ratio)
        font_img = ImageFont.truetype(font, font_size)

        # Calculate text bounding box
        text_bbox = draw.textbbox((0, 0), text, font=font_img)
        text_size = (text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1])

        # Calculate text position based on the provided ratios
        text_x = int(image_width * position_ratio[0])
        text_y = int(image_height * position_ratio[1])
        
        if is_genre:
            # Adjust vertical position for genre text
            text_y += text_size[1] + int(image_height * 0.04)

        text_position = (text_x, text_y)

        # Define the ratios for rectangle margin
        margin_ratio = 0.015  # 1.5% of the image dimensions
        radius = 40  # Define rectangle roundness

        # Calculate rectangle size based on text position and size
        rectangle_margin_width = image_width * margin_ratio
        rectangle_margin_height = image_height * margin_ratio

        rounded_rect_size = (
            text_position[0] - rectangle_margin_width,
            text_position[1] - rectangle_margin_height,
            text_position[0] + text_size[0] + rectangle_margin_width,
            text_position[1] + text_size[1] + rectangle_margin_height
        )

        draw_rounded_rectangle(draw, rounded_rect_size, radius, fill=rectangle_color)  # Draw rectangle
        draw.text(text_position, text, font=font_img, fill="black")  # Draw text

        return img
    def overlay_image(self, img: Image, overlayImage: Image,logoRatio=0.1,offsetPercentage=(0.05, 0.05)):
        # Calculate the new logo dimensions
        logoWidth = int(img.width * logoRatio)
        logoHeight = int(overlayImage.height * (logoWidth / overlayImage.width))

        # Resize the logo
        overlayImage = overlayImage.resize((logoWidth, logoHeight), Image.LANCZOS)

        # Calculate the proportional offset
        offset_x = int(img.width * offsetPercentage[0])
        offset_y = int(img.height * offsetPercentage[1])

        # Calculate position for the logo (bottom-right corner with offset)
        position = (img.width - logoWidth - offset_x, img.height - logoHeight - offset_y)

        # Overlay the logo on the image
        img.paste(overlayImage, position, overlayImage if overlayImage.mode == 'RGBA' else None)

        # Save the result
        return img


    
