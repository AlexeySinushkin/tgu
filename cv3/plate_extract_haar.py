import unittest

import cv2
import numpy as np

from augmentation import apply_augmentation

cascade = cv2.CascadeClassifier('Haar/haarcascade_license_plate_rus_16stages.xml')

class HaarRecognizeTests(unittest.TestCase):
    def test_detect(self):
        plate_img = cv2.imread('Haar/pattern_source.jpg')
        gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
        plates = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)

        for (x, y, w, h) in plates:
            cv2.rectangle(plate_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Detected", plate_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def test_augmentation(self):
        plate_img = cv2.imread('Haar/pattern_source.jpg')
        augmented_img = apply_augmentation(plate_img)
        augmented_img = cv2.GaussianBlur(augmented_img, (5, 5), 2)
        gray = cv2.cvtColor(augmented_img, cv2.COLOR_BGR2GRAY)
        plates = cascade.detectMultiScale(gray, scaleFactor=1.1)

        for (x, y, w, h) in plates:
            cv2.rectangle(plate_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Detected", augmented_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

