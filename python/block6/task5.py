# (8) Постройте график, который отображает две линии на одном поле, например,
# температуру и влажность за неделю. Используйте разные цвета и стили линий, добавьте
# легенду.
import matplotlib.pyplot as plt

humidity = [40, 45, 53, 56, 45, 40, 42]
temperature = [3.03, 3.68, 10.44, 8.32, 6.12, 6.92, 7.79]
days_of_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг',
         'Пятница', 'Суббота', 'Воскресение']


_, ax1 = plt.subplots(figsize=(10,6))
ax1.set_ylabel('Температура (°C)')
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.plot(days_of_week, temperature, label='Температура', color='blue', marker="o")

# Создадим вторую ось Y для влажности
ax2 = ax1.twinx()
ax2.set_ylabel('Влажность (%)', color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')
ax2.plot(days_of_week, humidity, label='Влажность', color='green', marker="x")

plt.grid(True)
# Показать легенды
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Добавим аннотации и другие элементы графика
plt.title('Изменение температуры и влажности за неделю', fontsize=14)
plt.tight_layout()

plt.show()