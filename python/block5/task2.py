# Напишите скрипт на Python, который создает DataFrame из двух списков: один список
# содержит имена студентов, другой — их оценки.
import pandas as pd

def get_students():
  student_names = pd.Series(['Aaron', 'Abram', 'Alice', 'Алиса', 'Антон'])
  student_degrees = pd.Series([4, 5, 3, 2, 1])

  return pd.DataFrame({'Имя': student_names,
                       'Оценка': student_degrees})

print(get_students())