# Напишите скрипт на Python, который создаст объект Series, содержащий данные о
# температуре за последние 7 дней. Используйте даты в качестве индексов.
import pandas as pd
import numpy as np
import datetime

today = datetime.date.today()
sub_day = lambda days_count: today - datetime.timedelta(days=days_count)
format_day = lambda date: date.strftime('%d.%m.%Y')
days = list(map(lambda offset: format_day(sub_day(offset)), range(5)))

temperatures = np.random.randint(-10, -5, size=(5))
s = pd.Series(temperatures, index=days)
print(s)