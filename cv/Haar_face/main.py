import matplotlib.pyplot as plt
import cv2
import numpy as np


class HaarFaceDetector:
    def __init__(self, xml_model):
        # Загрузка классификатора и создание каскадного объекта для распознавания лиц (указан путь к модели в вашей папке с данным ноутбуком)
        self.model = cv2.CascadeClassifier(xml_model)

    def detect_faces(self, image_path) -> (np.ndarray, int):
        # Чтение изображения
        original_image = cv2.imread(image_path)
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        # Конвертация изображения в градации серого
        grayscale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        detected_faces = self.model.detectMultiScale(grayscale_image)
        for (column, row, width, height) in detected_faces:
            cv2.rectangle(
                original_image,
                (column, row),
                (column + width, row + height),
                (0, 255, 0),
                2
            )
        return original_image, len(detected_faces)



def show_images(images):
    plt.subplot(121)
    plt.title(f"Найдено лиц {images[0][1]}")
    plt.imshow(images[0][0])
    plt.subplot(122)
    plt.title(f"Найдено лиц {images[1][1]}")
    plt.imshow(images[1][0])
    # plt.tight_layout()
    plt.show()

face_detector = HaarFaceDetector('haarcascade_frontalface_alt.xml')
image1, count1 = face_detector.detect_faces('face1.jpeg')
image2, count2 = face_detector.detect_faces('family.jpeg')
print(f"Первое изображение содержит лиц {count1}, второе {count2}")

show_images(((image1, count1), (image2, count2)))