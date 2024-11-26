# Загрузите данные в DataFrame из любого источника (например, CSV-файла) и измените
# названия столбцов, заменив их на более удобные или понятные.
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

try:
  # Загрузка данных
  url = 'https://raw.githubusercontent.com/pandas-dev/pandas/main/pandas/tests/io/data/csv/tips.csv'
  df = pd.read_csv(url)

  # Просмотр первых строк
  print(df.head())

  df.rename(columns={'total_bill': 'Сумма заказа', 'tip': 'Полученные чаевые',
                     'sex': 'Пол клиента', 'smoker': 'Курильщик',
                     'day': 'День недели'}, inplace=True)
  df['Пол клиента'] = df['Пол клиента'].apply(lambda sex: 'Мужской' if sex=='Male' else 'Женский')
  df['Процент от заказа'] = df['Полученные чаевые'] / df['Сумма заказа'] * 100
  print(df)
except Exception as ex:
  logging.error(ex)

