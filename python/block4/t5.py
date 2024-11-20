import numpy as np

# Напишите скрипт на Python, который:
# 1. Создаст два массива:
# a = [1, 2, 3, 4, 5]
# b = [5, 4, 3, 2, 1]
# 2. Вычислит сумму, разность, произведение и частное этих массивов.
# 3. Выведет результаты операций.

A = np.arange(1,6)
B = np.arange(5,0, -1)
print(A+B)
print(A-B)
print(A*B)
try:
  print(A/B)
except ZeroDivisionError as e:
  print("Деление на 0")