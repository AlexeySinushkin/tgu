# Круговая диаграмма распределения оценок студентов
# Напишите скрипт, который создает круговую диаграмму, отображающую
# распределение оценок студентов.
import matplotlib.pyplot as plt

values = [20, 100, 110, 40]
grades = ['Отличники', 'Хорошисты', 'Троишники', 'Отчисленные']
colors = ['yellow', 'pink', 'lightcoral', 'tomato']

fig = plt.figure(figsize=(10,6))
plt.title('Распределение оценок', fontsize=14)
# https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_features.html#sphx-glr-gallery-pie-and-polar-charts-pie-features-py
plt.pie(values, labels=grades, colors=colors)

plt.show()