import unittest

import cv2
import numpy as np

from augmentation import apply_augmentation

cascade = cv2.CascadeClassifier('Haar/haarcascade_license_plate_rus_16stages.xml')

def preprocess(image):
    gray = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
    # 1. Удаление "перцового" шума
    denoised = cv2.medianBlur(gray, 3)  # Можно 5, если сильно шумно
    # 2. (опц.) Билатеральная фильтрация — сохраняет края
    denoised = cv2.bilateralFilter(denoised, d=3, sigmaColor=50, sigmaSpace=50)
    # 3. (опц.) Увеличить контраст
    denoised = cv2.equalizeHist(denoised)
    plates = cascade.detectMultiScale(denoised, scaleFactor=1.1)

    plate_candidate = None
    for (x, y, w, h) in plates:
        aspect_ratio = w / float(h)
        if 3.7 < aspect_ratio < 5.0 and 140 < w < 250:
            plate_candidate = (x, y, w, h)
            cv2.rectangle(denoised, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return denoised, plate_candidate

class HaarRecognizeTests(unittest.TestCase):
    def test_detect(self):
        plate_img = cv2.imread('car1.jpg')
        gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
        plates = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)

        for (x, y, w, h) in plates:
            cv2.rectangle(plate_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Detected", plate_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def test_augmentation(self):
        plate_img = cv2.imread('car3.jpg')
        augmented_img = apply_augmentation(plate_img)
        gray = cv2.cvtColor(augmented_img, cv2.COLOR_BGR2GRAY)
        # 1. Удаление "перцового" шума
        denoised = cv2.medianBlur(gray, 3)  # Можно 5, если сильно шумно
        # 2. (опц.) Билатеральная фильтрация — сохраняет края
        denoised = cv2.bilateralFilter(denoised, d=3, sigmaColor=50, sigmaSpace=50)
        # 3. (опц.) Увеличить контраст
        denoised = cv2.equalizeHist(denoised)
        plates = cascade.detectMultiScale(denoised, scaleFactor=1.1)

        for (x, y, w, h) in plates:
            cv2.rectangle(denoised, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Detected", denoised)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

