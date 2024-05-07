import os
from PIL import Image
from typing import Union, Tuple

MAX_SIZE = (800, 800)


def open_image(image_path: str) -> Tuple[Image.Image, str]:
    """
    Opens an image from the specified path.
    """
    return Image.open(image_path), image_path


def resize_image(img: Image.Image, image_path: str) -> Tuple[Image.Image, str]:
    """
    Resizes an image if its dimensions exceed 800x800 pixels.
    """
    if img.height > MAX_SIZE[0] or img.width > MAX_SIZE[1]:
        output_size = MAX_SIZE
        img.thumbnail(output_size)
        img.save(image_path)
    return img, image_path


def convert_to_webp(img: Image.Image, image_path: str) -> Union[Tuple[str, str], Tuple[None, None]]:
    """
    Converts an image to WEBP format if it is not in this format.
    """
    first_path = image_path
    if img.format != 'WEBP':
        img = img.convert('RGB')
        image_path = os.path.splitext(image_path)[0]
        webp_path = f"{image_path}.webp"
        img.save(webp_path, 'WEBP')
        return os.path.relpath(webp_path, 'media'), first_path
    return None, None


def resize_and_convert_image(image_path: str) -> Tuple[str, str]:
    """
    Resizes and converts images to WEBP.
    """
    img, original_path = open_image(image_path)
    img, _ = resize_image(img, original_path)
    return convert_to_webp(img, original_path)


def handle_image(instance, img_instance) -> None:
    """
    Processes the model image, resizing it and converting it to WEBP format.
    """
    try:
        if img_instance:
            new_image_path, old_image_path = resize_and_convert_image(img_instance.path)
            if new_image_path:
                img_instance.name = new_image_path
                instance.save()
                if old_image_path and os.path.exists(old_image_path):
                    os.remove(old_image_path)
    except AttributeError:
        pass
