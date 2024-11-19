import numpy as np
import matplotlib.pyplot as plt

# Задание 1: Генерация сетки координат
# Напишите скрипт на Python, который:
# 1. Создаст два массива x и y, представляющих координаты от -5 до 5 с шагом 1.
# 2. Сгенерирует сетку координат с помощью функции "np.meshgrid".
# 3. Вычислит значения функции "z = x^2 + y^2" на этой сетке.
# 4. Выведет полученные массивы x, y и z.
# https://www.youtube.com/watch?v=7K_a1mmraHU

x = np.arange(-5, 6, 1)
y = np.arange(-5, 6, 1)
function = lambda x, y: x**2 + y**2

X, Y = np.meshgrid(x, y)
Z = function(X, Y)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z)
plt.show()
