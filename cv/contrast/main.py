# 1 Произвести линейную коррекцию контрастности изображения
# 2 Выравнивание гистограммы методами OpenCV

import cv2
import numpy as np
import copy
from matplotlib import pyplot


def to_grayscale(img: np.ndarray):
  R = 0.2989
  G = 0.5870
  B = 0.1140

  b = img[..., 0]
  g = img[..., 1]
  r = img[..., 2]
  result = B * b + G * g + R * r
  return result

def linear_contrast_correct(img: np.ndarray):
  return (img - img.min()) / (img.max() - img.min()) * 255

def imshow(img1, img2):
  _, axarr = pyplot.subplots(1, 2)
  axarr[0].imshow(img1, "gray")
  axarr[1].imshow(img2, "gray")
  pyplot.show()

def task1():
  # https://stepik.org/lesson/58402/step/6
  image_original = cv2.imread("tiger-low-contrast.png")
  image = copy.deepcopy(image_original)
  # для получения черно-белого изображения
  image = to_grayscale(image)
  image = linear_contrast_correct(image)
  imshow(image_original, image)

def task2():
  image_original = cv2.imread("tiger-low-contrast.png")
  # https://stackoverflow.com/questions/31998428/opencv-python-equalizehist-colored-image
  img_yuv = cv2.cvtColor(image_original, cv2.COLOR_BGR2YUV)

  # equalize the histogram of the Y channel (Y отвечает за яркость)
  img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])

  # convert the YUV image back to RGB format
  image = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
  imshow(image_original, image)

task1()
task2()