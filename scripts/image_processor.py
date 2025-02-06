from PIL import Image, ImageDraw, ImageFont, ImageFilter
from utility import draw_rounded_rectangle
import logging
from io import BytesIO


def convert_image(img, convert_to):
    try:
        img.convert(convert_to)
        return img
    except ValueError as e:
        raise ValueError(f"Invalid conversion mode: {convert_to}")

def apply_transformations( img):
    # Transform image by blurring, zooming, masking
    return img

def blur( img, blurFactor: float = 15):
    imgBlurred = img.filter(ImageFilter.GaussianBlur(blurFactor))
    return imgBlurred

def zoom( img, zoomFactor: float = 1.5) -> Image:
    imgZoomed = img.resize(
        (int(img.width * zoomFactor), int(img.height * zoomFactor)),
        resample=Image.LANCZOS
    )
    return imgZoomed

def square_image(img: Image)->Image:
    """
    Resize and crop the given image to make it square.

    Args:
        img (Image): The input image to be squared.

    Returns:
        Image: A new image object that is square with dimensions equal to the smaller of the width or height of the original image.
    """
    size = min(img.width, img.height)
    imgSquare = Image.new("RGB", (size, size))
    offset = ((size - img.width) // 2, (size - img.height) // 2)
    imgSquare.paste(img, offset)
    return imgSquare

def resize_to_square_canvas(img: Image):
    """
    Resize an image to fit within a square canvas of 1080x1080 pixels.

    This method creates a new square image with a white background and pastes
    the resized image in the center, maintaining the aspect ratio of the original image.

    Args:
        img (Image): The input image to be resized and centered on the square canvas.

    Returns:
        Image: A new image with the original image centered on a 1080x1080 pixel white canvas.
    """
    size = 1080
    imgSquare = Image.new("RGB", (size, size), (255, 255, 255))
    img.thumbnail((size, size), Image.LANCZOS)
    offset = ((size - img.width) // 2, (size - img.height) // 2)
    imgSquare.paste(img, offset)
    return imgSquare

def circle_mask(img: Image, borderColour: tuple, borderthicknessRatio: float = 0.04) -> Image:
    """
    Applies a circular mask to the given image and optionally adds a border around the circle.
    Args:
        img (Image): The input image to be masked.
        borderColour (tuple): The color of the border as an (R, G, B) tuple.
        borderthicknessRatio (float, optional): The thickness of the border as a fraction of the circle's diameter. Defaults to 0.04.
    Returns:
        Image: The resulting image with the circular mask and optional border applied.
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

def add_text(img, text, font, rectangle_color, is_genre=False)->Image:
    """
    Adds text with a rounded rectangle background to an image.
    Parameters:
    img (PIL.Image.Image): The image to which the text will be added.
    text (str): The text to be added to the image.
    font (str): The path to the font file to be used for the text.
    rectangle_color (str or tuple): The color of the rounded rectangle background.
    is_genre (bool, optional): If True, adjusts the vertical position for genre text. Defaults to False.
    Returns:
    PIL.Image.Image: The image with the added text and rounded rectangle background.
    """
    
    font_size = 32
    if is_genre:
        text_position = (50, 101)
    else:
        text_position = (50, 32)
    font_img = ImageFont.truetype(font, font_size)

    draw = ImageDraw.Draw(img) # Create a drawing object
    # Calculate text bounding box
    text_bbox = draw.textbbox((0, 0), text, font=font_img)
    text_size = (text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1])
    
    radius = 10  # Define rectangle roundness

    # Define margin around the text for the rectangle
    rectangle_margin_width = 9
    rectangle_margin_height = 9

    rounded_rect_size = (
        text_position[0] - rectangle_margin_width - 4 ,
        text_position[1] - rectangle_margin_height ,
        text_position[0] + rectangle_margin_width + text_size[0],
        text_position[1] + rectangle_margin_height +  38
    )

    draw_rounded_rectangle(draw, rounded_rect_size, radius, fill=rectangle_color)  # Draw rectangle

    draw.text(text_position, text, font=font_img, fill="black")  # Draw text
    return img


def overlay_image(img: Image, overlayImage: Image,logoRatio=0.1,offsetPercentage=(0.05, 0.05)):
    """
    Overlays an image (logo) onto another image at a specified position and size.

    Args:
        img (Image): The base image on which the overlay will be applied.
        overlayImage (Image): The image to overlay (logo).
        logoRatio (float, optional): The ratio of the logo's width relative to the base image's width. Default is 0.1.
        offsetPercentage (tuple, optional): The proportional offset (x, y) from the bottom-right corner of the base image. Default is (0.05, 0.05).

    Returns:
        Image: The resulting image with the overlay applied.
    """
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

def replace_colors_in_image(img_byte: BytesIO, color_map: dict)->Image:
    """
    Replace specific colors in an image with new colors as defined in a color map.
    Args:
        img_byte (BytesIO): A BytesIO object containing the image data.
        color_map (dict): A dictionary mapping original RGB color tuples to new RGB color tuples.
    Returns:
        Image: A PIL Image object with the colors replaced, or None if an error occurs.
    Raises:
        IOError: If the image cannot be opened or processed.
        Exception: For any other unexpected errors.
    """
    try:
        # Attempt to open the image
        with Image.open(img_byte) as img:
            img = img.convert("RGBA")
            logging.info("Image successfully opened and converted to RGBA mode.")

            # Get image data and attempt replacements
            data = img.getdata()
            new_data = [
                color_map.get(pixel[:3], pixel)  # Replace pixel if in color_map, else keep original
                for pixel in data
            ]
            
            # Apply modified pixel data
            img.putdata(new_data)
            logging.info("Color replacement completed successfully.")
            
            # Return a copy of the modified image outside the `with` block
            return img.copy()
            
    except IOError as e:
        logging.error(f"Failed to open or process image data: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None


    
def replace_colors_in_imageNew(img_byte: BytesIO, color_map: dict)->Image:
    """
    Replace specific colors in an image with new colors as defined in a color map.
    Args:
        img_byte (BytesIO): A BytesIO object containing the image data.
        color_map (dict): A dictionary mapping original RGB color tuples to new RGB color tuples.
    Returns:
        Image: A PIL Image object with the colors replaced, or None if an error occurs.
    Raises:
        IOError: If the image cannot be opened or processed.
        Exception: For any other unexpected errors.
    """
    try:
        # Attempt to open the image
        with Image.open(img_byte) as img:
            img = img.convert("RGBA")
            logging.info("Image successfully opened and converted to RGBA mode.")

            # Get image data and attempt replacements
            data = img.getdata()
            new_data = []
            for pixel in data:
                original_color = pixel[:3]
                if original_color in color_map:
                    new_color = color_map[original_color]
                    # Blend the original and new color for a smoother transition
                    blended_color = tuple(
                        int(original_color[i] * 0.5 + new_color[i] * 0.5) for i in range(3)
                    ) + (pixel[3],)  # Preserve the alpha channel
                    new_data.append(blended_color)
                else:
                    new_data.append(pixel)

            # Apply modified pixel data
            img.putdata(new_data)
            logging.info("Color replacement with smooth transition completed successfully.")
            
            # Return a copy of the modified image outside the `with` block
            return img.copy()
            
    except IOError as e:
        logging.error(f"Failed to open or process image data: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None