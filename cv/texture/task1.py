from skimage import io, filters
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
from matplotlib import pyplot as plt
from skimage.feature import peak_local_max

def get_voronoi_diagram(img_path):
  # Загрузка изображения (не забудьте загрузить изображение в папку colab слева)
  img = io.imread(img_path)

  # Проверка размеров изображения
  print(img.shape)

  # отбираем тольк один цветовой канал для корректной работы (третий индекс 0 соотвествует первому по порядку каналу)
  img = img[:, :, 0]
  print(img.shape)

  # Шаг 1 - Применение гауссового размытия для усреднения локальных вариаций интенсивности
  img_blurred = filters.gaussian(img, sigma=9)  # Гауссовое размытие с заданным значением sigm


  # Шаг 2: Нахождение точек, представляющих каждый объект, для использования в Вороного
  # Нахождение локальных максимумов на изображении
  coordinates = peak_local_max(
      img_blurred,
      min_distance=20,
      exclude_border=False
  )

  # Шаг 3: Создание диаграммы вороного
  vor3 = Voronoi(coordinates)
  return voronoi_plot_2d(vor3)

leopard_diagram = get_voronoi_diagram('leopard.jpg')
leopard_diagram.show()
plt.show()


