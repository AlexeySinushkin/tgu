# Добавьте новый столбец с возрастом студентов в DataFrame из предыдущего задания.
# Используйте методы head() и tail(), чтобы вывести на экран первые и последние строки
# DataFrame.
import pandas as pd

from task2 import get_students

df = get_students()
age = pd.Series(range(16, 21))
df['Возраст'] = age

print(df.head(1))
print(df.tail(1))
