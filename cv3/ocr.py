import unittest

import numpy as np
from matplotlib import pyplot as plt
import cv2
from easyocr import easyocr
import re



# убираем шум
def prepare(plate_img):
    img_gray = cv2.cvtColor(plate_img.copy(), cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(img_gray, (5, 5), 1)
    threshold, binary_img = cv2.threshold(blurred, 80, 255, cv2.THRESH_BINARY)

    # Создаем ядро (структурный элемент) для морфологических операций — квадрат 2x2 пикселей
    kernel = np.ones((2, 2), np.uint8)
    # 2) Дилатация — расширяет белые области, увеличивает объекты, заполняет пробелы
    dilation = cv2.dilate(binary_img, kernel, iterations=1, borderType=cv2.BORDER_CONSTANT)
    return dilation

def clean_text(text):
    # Keep only letters and digits
    cleaned = re.sub(r'[^A-Za-zА-Яа-яЁё0-9]', '', text)

    # Safety check
    if len(cleaned) <= 5:
        return cleaned  # Too short to split

    # Split after index 5
    return cleaned[:6] + ' ' + cleaned[6:]

def get_text(plate_img):
    reader = easyocr.Reader(['ru'])
    results = reader.readtext(plate_img)
    text_string = ' '.join([res[1] for res in results])
    text_string = clean_text(text_string)
    return text_string


class OcrTests(unittest.TestCase):
    def test_prepare_img(self):
        plate_img = cv2.imread('test-resources/plate3.jpg')
        f, axes = plt.subplots(1, 2, figsize=(10, 5))
        axes[0].imshow(plate_img)
        axes[1].imshow(prepare(plate_img))
        plt.show()
    def test_ocr(self):
        plate_img = cv2.imread('test-resources/plate3.jpg')
        text = get_text(prepare(plate_img))
        print(text)
