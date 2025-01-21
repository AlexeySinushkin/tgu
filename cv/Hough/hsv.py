# Для работы с массивами и отображением
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import imread
import cv2


def cv2_show_image(image):
    cv2.imshow("Изображение", image)
    while True:
        key = cv2.waitKey(1)
        if key == 27:
            cv2.destroyAllWindows()


image_path = "balls.png"
# c помощью GIMP поводив по зеленому шарику выяснил что компоненты меняют свои значения в разном масштабе
# H 70-90
# S 85-87
# V 65-90


base_image = cv2.imread(image_path)
base_RGB = cv2.imread(image_path)
# Пробуем просто взять красный канал
image_HSV = cv2.cvtColor(base_image, cv2.COLOR_BGR2HSV)

# маски для красного цвета
mask = cv2.inRange(image_HSV, (70,85,65), (90,87,90))
onlyGreen = cv2.bitwise_and(image_HSV, image_HSV, mask=mask)

cv2_show_image(onlyGreen)



