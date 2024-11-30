# Столбчатый график количества студентов на разных факультетах
# Постройте столбчатый график, отображающий количество студентов в разных
# факультетах. Используйте разные цвета для каждого столбца.
import matplotlib.pyplot as plt

values = [200, 300, 250, 400]
names = ['Энергетический', 'Исторический', 'Филологический', 'Кибернетический']
colors = ['yellow', 'pink', 'lightcoral', 'tomato']

fig = plt.figure(figsize=(10,6))
plt.title('Количества студентов на разных факультетах', fontsize=14)
plt.xlabel('Факультет', fontsize=10)
plt.ylabel('Количество студентов', fontsize=10)
# https://matplotlib.org/stable/gallery/color/named_colors.html
plt.bar(names, values, label=names, color=colors)


plt.show()