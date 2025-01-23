import io
import uuid

import cv2
from PIL import Image
from config import settings

def load_image(file_name) -> io.BytesIO:
    image = Image.open("{}/{}".format(settings.images_dir, file_name))
    imgio = io.BytesIO()
    image.save(imgio, 'PNG')
    imgio.seek(0)
    return imgio

def save_image(frame) -> str:
    file_name = f"{uuid.uuid4()}.png"
    cv2.imwrite("{}/{}".format(settings.images_dir, file_name), frame)
    return file_name