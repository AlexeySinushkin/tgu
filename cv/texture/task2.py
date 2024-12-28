import cv2
import numpy as np
from skimage.feature import local_binary_pattern
import matplotlib.pyplot as plt

def get_lbp(path_to_image):
  # Параметры LBP
  radius = 3  # Радиус для поиска соседних пикселей
  n_points = 8 * radius  # Количество точек по окружности

  # Загружаем изображение и преобразуем его в оттенки серого
  image = cv2.imread(path_to_image, cv2.IMREAD_GRAYSCALE)
  plt.imshow(image, cmap='gray')
  # Применение LBP к изображению
  lbp = local_binary_pattern(image, n_points, radius, method="uniform")

  # Построение гистограммы LBP для всего изображения
  # Уникальные значения и их частоты (гистограмма)
  lbp_hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0, n_points + 3), range=(0, n_points + 2))

  # Нормализуем гистограмму
  lbp_hist = lbp_hist.astype("float")
  lbp_hist /= (lbp_hist.sum() + 1e-6)

  return lbp, lbp_hist

lbp, lbp_hist = get_lbp('brick_wall.jpg')
print("LBP Histogram:", lbp_hist)
plt.imshow(lbp, cmap="gray")
plt.show()