from pickletools import uint8

# https://mass-images.pro/ru/batch/tpl/noise
# https://docs.google.com/presentation/d/1dLd-_1r5apaGGJYj_WFn91hWmhtOo3iL0ERIaS23IPY/edit#slide=id.g3120aa44f24_0_22
# https://www.geeksforgeeks.org/python-opencv-filter2d-function/
# Написать программу которая выполняет фильтрацию изображения низкочастотным, высокочастотным и нелинейным медианным фильтром

import cv2
import numpy as np
import copy

from erfa import dt_type
from matplotlib import pyplot

def imshow(img):
  grid_size = int(len(img)/2)
  _, axarr = pyplot.subplots(grid_size, grid_size)
  for i in range(len(img)):
    row_index = int(i/grid_size)
    col_index = i - (row_index*grid_size)
    axarr[row_index, col_index].imshow(img[i])

  pyplot.show()


# Низкочастотный
kernel_box = np.ones((7, 7), np.float32) / 50
image_poisson = cv2.imread("1_impulse.png")
image_box = cv2.filter2D(image_poisson, ddepth=-1, kernel=kernel_box)

# Высокочастотный (Собель, Превит, Робертс)
kernel_roberts_x = np.array([[1,0], [0,-1]])
kernel_roberts_y = np.array([[0,1], [-1,0]])
image_roberts_x = cv2.filter2D(image_box, ddepth=-1, kernel=kernel_roberts_x)
image_roberts_y = cv2.filter2D(image_box, ddepth=-1, kernel=kernel_roberts_y)
image_roberts_hypot = np.hypot(image_roberts_x, image_roberts_y)
scale = lambda x: ((x - x.min()) / (x.max() - x.min()) * 255).astype(int)
image_roberts = scale(image_roberts_hypot)

# Медианный
image_median = cv2.medianBlur(image_poisson, 5)

imshow([image_poisson, image_box, image_roberts, image_median])

# cv2.imshow('Original', image_poisson)
# cv2.imshow('Kernel Blur', image)
# cv2.waitKey()
# cv2.destroyAllWindows()