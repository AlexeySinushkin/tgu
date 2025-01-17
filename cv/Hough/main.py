# Для работы с массивами и отображением
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import imread
# version=4.10.0
import cv2


# Алогритм Хафа для поиска линий.
def HighlightColour(path):
    baseImage = cv2.imread(path)
    image = cv2.cvtColor(baseImage, cv2.COLOR_BGR2RGB)

    #cv2.imshow("Оригнальное изображение", image)

    # Пробуем просто взять красный канал
    B,G,R = cv2.split(image)
    # Отсекаем пиксели, у которых значение меньше 200
    redImage = np.zeros(image.shape)
    redImage[(R > 200), (B>200) ] = [255, 255, 255]
    cv2.imshow("Изображение с отсеченными цветами R", redImage)


#получение усредненного цвета внутри круга
def get_circle_avg_colour(image: np.ndarray, center: (int, int), half_radius: int):
    # colors = np.ndarray((3, 12)).astype('uint8')
    colors = np.ndarray((12,3), dtype='uint8')
    for ang, i in zip(range(0, 360, 30), range(0,12)):
        th = np.radians(ang)
        x = int(half_radius * np.sin(th) + center[0])
        y = int(half_radius * np.cos(th) + center[1])
        pixel_value = image[y, x, :]
        colors[i] = pixel_value
        cv2.circle(image, (x, y), 2, (0, 255, 0), 2)
    return colors.mean(dtype='uint8')

def HoughCircleTransform(path):
    baseImage = cv2.imread(path)
    image = cv2.cvtColor(baseImage, cv2.COLOR_BGR2RGB)

    resultImage = image.copy()
    imageGray = cv2.cvtColor(resultImage, cv2.COLOR_RGB2GRAY)
    width = imageGray.shape[1]
    minDist = int(width/30)
    minRadius = int(width/30)
    maxRadius = int(width/10)
    circles = cv2.HoughCircles(imageGray,cv2.HOUGH_GRADIENT,1,minDist,
                             param1=80,param2=20,
                             minRadius=minRadius,maxRadius=maxRadius)
    circle_colours = []
    if circles is not None:
        circles = np.around(circles).astype('uint16')
        for x, y, r in circles[0, :]:
            cv2.circle(resultImage,(x,y), r,(0,255,0),2)
            circle_colours.append(get_circle_avg_colour(resultImage, (x,y), int(r/2)))
    return resultImage

image = HoughCircleTransform("balls.png")
cv2.imshow("Изображение с отсеченными цветами R", image)

while True:
    key = cv2.waitKey(1)
    if key == 27:
        cv2.destroyAllWindows()