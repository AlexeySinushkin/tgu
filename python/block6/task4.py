# Диаграмма рассеяния зависимости между двумя переменными
# Используйте функцию scatter() для построения диаграммы рассеяния,
# отображающей зависимость между двумя переменными.
import matplotlib.pyplot as plt

exam_number = [1, 6, 2, 4, 4, 1, 3, 1, 3]
score = [93,87,70, 62, 86, 73, 80, 96, None]

plt.scatter(exam_number, score, alpha=0.5)
plt.show()
