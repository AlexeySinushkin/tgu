import numpy as np #для матричных вычислений
import pandas as pd #для анализа и предобработки данных
import matplotlib.pyplot as plt #для визуализации
import seaborn as sns #для визуализации
from fontTools.merge.util import equal
from sklearn import linear_model #линейные модели
from sklearn import metrics #метрики
#%matplotlib inline
plt.style.use('seaborn-v0_8')


column_names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']
boston_data = pd.read_csv('data/Boston.csv', header=None, delimiter=r"\s+", names=column_names)
print(boston_data.info())
print(boston_data.head())

def print_correlation():
  #Вычисляем модуль корреляции
  corr_with_target = boston_data.corr()['MEDV'].abs().sort_values()
  #Удаляем корреляцию целевой переменной с самой собой
  corr_with_target = corr_with_target.drop('MEDV')
  #Строим столбчатую диаграмму корреляций
  _, ax = plt.subplots(figsize=(10, 5)) #фигура+координатная плоскость
  ax.bar(corr_with_target.index, corr_with_target.values) #столбчатая диаграмма
  ax.set_title('Correlations with target') #название графика
  ax.set_xlabel('Feature') #название оси x
  ax.set_ylabel('Сorrelation coefficient') #название оси y
  plt.show()

def linear_regression(X, y):
  # Создаём вектор из единиц
  ones = np.ones(X.shape[0])
  # Добавляем вектор к таблице первым столбцом
  X = np.column_stack([ones, X])
  M0 = np.linalg.matmul(X.T, X)
  #M1 = X.T @ X
  # Вычисляем обратную матрицу Q
  Q = np.linalg.inv(M0)
  # Вычисляем вектор коэффициентов
  w = Q @ X.T @ y
  return w

X = boston_data[['LSTAT']] #матрица наблюдений
y = boston_data['MEDV'] #вектор правильных ответов


#Вычисляем параметры линейной регрессии
w = linear_regression(X, y)
#Выводим вычисленные значения параметров в виде вектора
print('Vector w: {}'.format(w))
#Выводим параметры с точностью до двух знаков после запятой
print('w0: {:.2f}'.format(w[0]))
print('w1: {:.2f}'.format(w[1]))

# y=kx + b
k=w[1]
b=w[0]
#Делаем предсказание для всех объектов из таблицы
y_predict = k * X + b
y_true = y


_, ax = plt.subplots(figsize=(8, 4))  # фигура + координатная плоскость
ax.scatter(X, y_true, alpha=0.7, label='Реальные данные')  # диаграмма рассеяния
ax.plot(X, y_predict, color='black', label='Предсказание')  # линейный график
ax.set_xlabel("средняя стоимость жилья")  # название оси абсцисс
ax.set_ylabel("процент населения с низким статусом")  # название оси ординат
ax.legend(facecolor='white', fontsize=11)  # легенда
#plt.show()

new_data = {
'CRIM':         [0.35114],
'ZN':           [0.00000],
'INDUS':        [7.38000],
'CHAS':         [0.00000],
'NOX':          [0.49300],
'RM':          [6.04100],
'AGE':         [49.90000],
'DIS':          [4.72110],
'RAD':         [5.00000],
'TAX':        [287.00000],
'PTRATIO':     [19.60000],
'B':          [396.90000],
'LSTAT':        [7.70000]
}

new_df = pd.DataFrame(data=new_data)

#Создаём объект класса LinearRegression
lr_lstat = linear_model.LinearRegression()
#Обучаем модель — ищем параметры по МНК
lr_lstat.fit(X, y)
print('w0: {}'.format(lr_lstat.intercept_)) #свободный член w0
print('w1: {}'.format(lr_lstat.coef_)) #остальные параметры модели w1, w2, ..., wm

#По всем колонкам
#Составляем список факторов (исключили целевой столбец)
features = boston_data.drop('MEDV', axis=1).columns
#Составляем матрицу наблюдений X и вектор ответов y
X = boston_data[features]
y = boston_data['MEDV']
#Создаём объект класса LinearRegression
lr_full = linear_model.LinearRegression()
#Обучаем модель — ищем параметры по МНК
lr_full.fit(X, y)
print(lr_full.predict(new_df))


