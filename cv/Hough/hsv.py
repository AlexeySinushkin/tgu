# Для работы с массивами и отображением
import numpy as np
import cv2


def cv2_show_image(image):
    cv2.imshow("Изображение", image)
    while True:
        key = cv2.waitKey(1)
        if key == 27:
            cv2.destroyAllWindows()


def cv2_find_by_colour(low, high):
    th = (low[0], high[0])
    ts = (low[1], high[1])
    tv = (low[2], high[2])

    base_image = cv2.imread(image_path)
    image_RGB = cv2.cvtColor(base_image, cv2.COLOR_BGR2RGB)
    image_HSV = cv2.cvtColor(base_image, cv2.COLOR_BGR2HSV)

    for x in range(0, image_HSV.shape[1]):
        for y in range(0, image_HSV.shape[0]):
            h, s, v, = image_HSV[y, x]
            if not(th[0] < h < th[1] and ts[0] < s < ts[1] and tv[0] < v < tv[1]):
                image_RGB[y, x] = (0, 0, 0)
    return image_RGB

def find_countur(image_RGB):
    gray = cv2.cvtColor(image_RGB, cv2.COLOR_RGB2GRAY)
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    #cv2_show_image(threshold)

    # Поиск контура
    counturResult = np.zeros(image_RGB.shape, dtype = np.uint8)
    copyImage = image_RGB.copy()

    contours, hierarchy = cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(counturResult, contours[1:3], -1, (0, 0, 255), 3)
    cv2.drawContours(copyImage, contours, -1, (0, 0, 255), 3)

    #print("Контур")
    #cv2_show_image(cv2.hconcat((counturResult, copyImage)))

    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(counturResult, cv2.MORPH_CLOSE, kernel)
    return opening



# c помощью GIMP поводив по зеленому шарику выяснил что компоненты меняют свои значения в разном масштабе
# H 70-90
# S 85-87
# V 65-90
# Problem 1 : Different applications use different scales for HSV. For example gimp uses H = 0-360, S = 0-100 and V = 0-100.
# But OpenCV uses H: 0-179, S: 0-255, V: 0-255.
# https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv
def gimp_to_open_cv_hsv(hsv):
    return hsv[0]*179/360,hsv[1]*255/100,hsv[2]*255/100


image_path = "balls.png"
low = gimp_to_open_cv_hsv([65, 82, 50])
high = gimp_to_open_cv_hsv([100, 89, 90])

image_RGB = cv2_find_by_colour(low, high)
#cv2_show_image(image_RGB)
countur = find_countur(image_RGB)
cv2_show_image(countur)