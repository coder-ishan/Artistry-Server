import os
from PIL import Image, ImageDraw, ImageFont
from IPython.display import display

def create_text_image(text, font_path, image_size=(300, 400), text_color=(0, 0, 0, 255)):
    """
    Create an image with specified text using a TTF font file on a transparent background and save it to the Downloads folder.
    Dynamically adjusts font size to fit text within the image.
    :param text: Text to render.
    :param font_path: Path to the TTF font file.
    :param image_size: Tuple of (width, height) of the image.
    :param text_color: RGBA color for the text.
    :param file_name: Name of the output file.
    """
    
    image = Image.new("RGBA", image_size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    
    max_width, max_height = image_size
    font_size = 1  # Start with a small font size
    font = ImageFont.truetype(font_path, font_size)

    while True:
        text_width, text_height = draw.textsize(text, font=font)
        if text_width >= max_width or text_height >= max_height:
            font_size -= 1  # The last font size that fit
            font = ImageFont.truetype(font_path, font_size)
            break
        font_size += 1
        font = ImageFont.truetype(font_path, font_size)

    
    text_width, text_height = draw.textsize(text, font=font)
    text_x = (max_width - text_width) // 2
    text_y = (max_height - text_height) // 2

    
    draw.text((text_x, text_y), text, font=font, fill=text_color)

    return image
