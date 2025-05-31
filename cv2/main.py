import cv2
import numpy as np
from matplotlib import pyplot as plt

def resize(img, size=(100, 100)):
    old_h, old_w = img.shape[:2]
    new_h, new_w = size

    # Выбор интерполяции
    if old_h > new_h or old_w > new_w:
        interp = cv2.INTER_AREA  # лучше для уменьшения
    else:
        interp = cv2.INTER_CUBIC  # лучше для увеличения

    # Создаем холст из нулей (чёрный фон)
    new_img = np.zeros((new_h, new_w, img.shape[2]), dtype=img.dtype)

    ar = old_h / old_w
    if ar > 1:  # вертикальное изображение
        factor = new_h / old_h
        resize_h = new_h
        resize_w = int(old_w * factor)
    else:  # горизонтальное изображение или квадрат
        factor = new_w / old_w
        resize_w = new_w
        resize_h = int(old_h * factor)

    resized_img = cv2.resize(img, (resize_w, resize_h), interpolation=interp)

    # Вставляем центрированное изображение на холст
    start_ymin = max((new_h - resize_h) // 2, 0)
    start_xmin = max((new_w - resize_w) // 2, 0)

    new_img[start_ymin:start_ymin + resize_h, start_xmin:start_xmin + resize_w] = resized_img

    return new_img



img = cv2.imread('archive/bleached_corals/876246000_b90c98b818_o.jpg')
new_img = resize(img)

plt.imshow(new_img[...,::-1])
plt.show()