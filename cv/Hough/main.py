# Для работы с массивами и отображением
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import imread
import cv2


# получение усредненного цвета внутри круга
def get_circle_avg_colour(image: np.ndarray, center: (int, int), half_radius: int):
    # colors = np.ndarray((3, 12)).astype('uint8')
    colors = np.ndarray((12, 3), dtype='uint8')
    for ang, i in zip(range(0, 360, 30), range(0, 12)):
        th = np.radians(ang)
        x = int(half_radius * np.sin(th) + center[0])
        y = int(half_radius * np.cos(th) + center[1])
        pixel_value = image[y, x, :]
        colors[i] = pixel_value
        cv2.circle(image, (x, y), 2, (0, 255, 0), 2)
    return colors.mean(axis=0).astype('uint8')


def HoughCircleTransform(path):
    baseImage = cv2.imread(path)
    image = cv2.cvtColor(baseImage, cv2.COLOR_BGR2RGB)

    resultImage = image.copy()
    imageGray = cv2.cvtColor(resultImage, cv2.COLOR_RGB2GRAY)
    width = imageGray.shape[1]
    minDist = int(width / 30)
    minRadius = int(width / 30)
    maxRadius = int(width / 10)
    circles = cv2.HoughCircles(imageGray, cv2.HOUGH_GRADIENT, 1, minDist,
                               param1=80, param2=20,
                               minRadius=minRadius, maxRadius=maxRadius)
    circle_colours = []
    if circles is not None:
        circles = np.around(circles).astype('uint16')
        for x, y, r in circles[0, :]:
            cv2.circle(resultImage, (x, y), r, (0, 255, 0), 2)
            circle_colours.append(get_circle_avg_colour(resultImage, (x, y), int(r / 2)))
    return resultImage, circle_colours


def highlightColour(path, target_colour, threshold=40):
    base_image = cv2.imread(path)
    image = cv2.cvtColor(base_image, cv2.COLOR_BGR2RGB)

    tr, tg, tb = target_colour.astype('int16')
    left = lambda target: target - threshold if target - threshold > 0 else 0
    right = lambda target: target + threshold if target + threshold < 255 else 255

    for x in range(0, image.shape[1]):
        for y in range(0, image.shape[0]):
            r, g, b = image[y, x, :]
            if left(tr) <= r <= right(tr) and left(tg) <= g <= right(tg) and left(tb) <= b <= right(tb):
                image[y, x] = (r, g, b)
            else:
                image[y, x] = 0
    # Морфологическая операция закрытия
    kernel = np.ones((5, 5), np.uint8)
    closing = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    #cv2.imshow("Изображение", closing)
    return closing

def cv2_show_image(image):
    # cv2.imshow("Изображение", image)
    while True:
        key = cv2.waitKey(1)
        if key == 27:
            cv2.destroyAllWindows()

image_path = "balls.png"
# Находим круги с помощью алгоритма Хаффа
image, circle_colours = HoughCircleTransform(image_path)


# Теперь пытаемся найти те-же самые круги, зная их цвет
image0 = highlightColour(image_path, circle_colours[0])
image1 = highlightColour(image_path, circle_colours[1])
image2 = highlightColour(image_path, circle_colours[2])
image3 = highlightColour(image_path, circle_colours[3], threshold=60)
image4 = highlightColour(image_path, circle_colours[4], threshold=50)
image5 = highlightColour(image_path, circle_colours[5], threshold=65)

fig, axes = plt.subplots(3, 2, figsize=(20, 60))
axes[0, 0].imshow(image0)
axes[0, 1].imshow(image1)
axes[1, 0].imshow(image2)
axes[1, 1].imshow(image3)
axes[2, 0].imshow(image4)
axes[2, 1].imshow(image5)
# plt.tight_layout()
plt.show()


