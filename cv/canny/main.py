import logging
import numpy as np
from matplotlib import pyplot
import cv2

# Sobel  https://stackoverflow.com/questions/51167768/sobel-edge-detection-using-opencv
# NMS https://en.wikipedia.org/wiki/Edge_detection#Canny https://www.geeksforgeeks.org/what-is-non-maximum-suppression/

logging.basicConfig(level=logging.DEBUG, filename='app.log', encoding='UTF-8',
                    filemode='w', format='%(levelname)s: %(message)s')


def to_grayscale(img: np.ndarray):
  R = 0.2989
  G = 0.5870
  B = 0.1140

  b = img[..., 0]
  g = img[..., 1]
  r = img[..., 2]
  result = B * b + G * g + R * r
  return result

def to_red(img: np.ndarray):
  return img[..., 2]

def to_green(img: np.ndarray):
  return img[..., 1]

def to_blue(img: np.ndarray):
  return img[..., 0]

def hypot(imgX, imgY):
  scale = lambda x: (x - x.min()) / (x.max() - x.min()) * 255
  return scale(np.hypot(imgX, imgY))


def imshow(img):
  # pyplot.figure(figsize=(20, 20))
  pyplot.imshow(img, "gray")
  pyplot.xticks([])
  pyplot.yticks([])
  pyplot.show()


def nms(img, theta):
  height, width = img.shape
  print(f'height-{height} width-{width}')
  result = np.zeros((height, width), dtype=np.int32)
  angle = theta * 180.0 / np.pi
  angle[angle < 0] += 180

  for h in range(1, height - 1):
    for w in range(1, width - 1):
      q = 0
      r = 0
      # ближе к горизонту
      if (0 <= angle[h, w] < 22.5) or (157.5 <= angle[h, w] <= 180):
        r = img[h, w - 1]  # левей
        q = img[h, w + 1]  # правей
      # диагональ
      elif 22.5 <= angle[h, w] < 67.5:
        r = img[h - 1, w + 1]  # выше правей
        q = img[h + 1, w - 1]  # ниже левей
      # ближе к вертикалу (90)
      elif 67.5 <= angle[h, w] < 112.5:
        r = img[h - 1, w]  # выше
        q = img[h + 1, w]  # ниже
      # диагональ
      elif 112.5 <= angle[h, w] < 157.5:
        r = img[h + 1, w + 1]  # ниже правей
        q = img[h - 1, w - 1]  # выше левей

      # если целевая точка контрастней смежных по нормали к границе
      if img[h, w] >= q and img[h, w] >= r:
        result[h, w] = img[h, w]
      else:
        result[h, w] = 0

  return result


# Двойная пороговая фильтрация. Если значение пикселя
# выше верхней границы – он принимает максимальное значение (граница считается
# достоверной), если ниже – пиксель подавляется, точки со значением, попадающим в
# диапазон между порогов, принимают фиксированное среднее значение (они будут
# уточнены на следующем этапе).
def threshold(img, lowRatio=0.1, highRatio=0.2, weak=150, strong=255):
  height, width = img.shape
  result = np.zeros((height, width), dtype=np.int32)
  high_threshold = img.max() * highRatio
  low_threshold = high_threshold * lowRatio

  strong_i, strong_j = np.where(img >= high_threshold)
  weak_i, weak_j = np.where((img < high_threshold) & (img > low_threshold))

  result[strong_i, strong_j] = strong
  result[weak_i, weak_j] = weak
  return result


# Трассировка. те пиксела, что были слабыми становятся либо 0 либо сильными
# в зависимости от соседей
def hysteresis(img, weak=150, strong=255):
  height, width = img.shape
  result = img.copy()
  for h in range(1, height - 1):
    for w in range(1, width - 1):
      if img[h, w] == strong:
        result[h, w] = strong
      elif img[h, w] == weak:
        if (
            (img[h + 1, w + 1] == strong or img[h - 1, w - 1] == strong) or
            (img[h, w + 1] == strong or img[h, w - 1] == strong) or
            (img[h + 1, w] == strong or img[h - 1, w] == strong) or
            (img[h + 1, w-1] == strong or img[h - 1, w+1] == strong)
        ):
          result[h, w] = strong
        else:
          result[h, w] = 0
      elif img[h, w] > 0 :
        print('{}'.format(img[h,w]))
  return result


def apply_pipeline(img):
  blur_image = cv2.GaussianBlur(img, ksize=(29, 29), sigmaX=2, sigmaY=2)
  grad_x = cv2.Sobel(blur_image, cv2.CV_64F, 1, 0)
  grad_y = cv2.Sobel(blur_image, cv2.CV_64F, 0, 1)
  grad_norm = hypot(grad_x, grad_y)
  theta = np.arctan2(grad_y, grad_x)
  img_nms = nms(grad_norm, theta)
  img_threshold = threshold(img_nms)
  img_hyst = hysteresis(img_threshold)
  return img_hyst


def show_1():
  image = cv2.imread("images/1.png")
  red = to_red(image)
  red = apply_pipeline(red)
  imshow(red)

def show_street():
  image = cv2.imread("images/poster.png")
  image = to_grayscale(image)
  image = apply_pipeline(image)
  imshow(image)

def show_stadium():
  image = cv2.imread("images/stadium.jpg")
  image = to_grayscale(image)
  image = apply_pipeline(image)
  imshow(image)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
  #show_1()
  show_street()
  #show_stadium()

