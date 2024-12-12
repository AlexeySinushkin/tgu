import numpy as np #для матричных вычислений
import pandas as pd #для анализа и предобработки данных
from sklearn import linear_model #линейные модели

column_names=['R&D Spend', 'Administration', 'Marketing Spend', 'Profit']
data = pd.read_csv('data/50_Startups.csv', usecols=column_names)
print(data.info())
print(data.head())

features = data.drop('Profit', axis=1).columns
#Составляем матрицу наблюдений X и вектор ответов y
X = data[features]
Y = data['Profit']

lr_lstat = linear_model.LinearRegression()
#Обучаем модель — ищем параметры по МНК
lr_lstat.fit(X, Y)
print('w0: {:.2f}'.format(lr_lstat.intercept_))
print(f'{features}')
print('wn: {}'.format(lr_lstat.coef_))

Y_PREDICT = lr_lstat.predict(data[features])
errors = (Y - Y_PREDICT)/Y*100
print(errors)