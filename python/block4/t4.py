import numpy as np

# Напишите скрипт на Python, который:
# 1. Создаст массив чисел от 10 до 19.
# 2. Выведет элементы с 3-го по 7-й (включительно).
# 3. Заменит элементы с 5-го по 8-й на 0.
# 4. Выведет измененный массив.
# https://stackoverflow.com/questions/11364533/why-are-pythons-slice-and-range-upper-bound-exclusive

x = np.arange(10, 20)
print(x[3:8])
x[5:8] = 0
print(x)