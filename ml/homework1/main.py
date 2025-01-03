import numpy as np #для матричных вычислений
import pandas as pd #для анализа и предобработки данных
import matplotlib.pyplot as plt #для визуализации
import seaborn as sns #для визуализации
from pandas.core.util.numba_ import get_jit_arguments

from sklearn import metrics #метрики
from sklearn import model_selection #методы разделения и валидации
from sklearn import ensemble #ансамбли

plt.style.use('seaborn-v0_8') #стиль отрисовки seaborn

#Таблица успешно прочитана, используется правильный путь к файлу, данные корректно выведены на экран.
df = pd.read_csv('data/online_shoppers_intention.csv')
print(df.head())

#Размер таблицы корректно выведен с использованием подходящей функции (например, .shape), и результат соответствует ожиданиям.
print(f"Строк {df.shape[0]}. Столбцов {df.shape[1]}")
assert df.shape[0] > 12000 and df.shape[1] == 18

#Проверка выполнена корректно, использованы подходящие методы (например, .isnull().sum() или .info()), вывод результатов ясен и понятен.
nulls = df.isnull().sum()
print(nulls)
for col, sum_of_nulls in nulls.items():
    assert sum_of_nulls == 0, f"Имеются пропуски в колонке {col}"

#График построен корректно, выбран подходящий тип визуализации (например, столбчатая диаграмма или круговая диаграмма),
# соотношение классов отображено наглядно.

def show_cat_relations():
    types = df.dtypes
    #Категориальные признаки
    cat_features = list(types[(types == 'object')].index)
    print(cat_features) # ['Month', 'VisitorType']
    n = len(cat_features) #число категориальных признаков
    fig, axes = plt.subplots(1, 2, figsize=(40, 20))
    #Строим столбчатую диаграмму для категории Месяц
    sns.barplot(data=df, x=cat_features[0], y='Revenue', ax=axes[0])
    #Строим столбчатую диаграмму для категории Тип посетителя
    sns.barplot(data=df, x=cat_features[1], y='Revenue', ax=axes[1])

    plt.tight_layout()
    plt.show()

#show_cat_relations()
#по столбчатым диаграммам видим что максимум приходится на конец года - Октябрь, Ноябрь, Декабь
# в Январе и феврале - минимум продаж - этот признак отбрасывать нельзя
#по типу клиента связь выражена не так сильно как по месяцам, но все-же есть. (тоже не отбрасываем)

#Категориальные признаки корректно закодированы с использованием функции pd.get_dummies(), преобразование выполнено без ошибок.
print(df.describe(include='object'))
df_dummies = pd.get_dummies(df)
print(f"Описание после преобразования категориальных признаков. Количество колонок {df_dummies.dtypes.shape}")
print(df_dummies.dtypes)

#Итак, нам необходимо предсказать целевую переменную Revenue — признак покупки. Целевой признак является
# бинарным категориальным, то есть мы решаем задачу бинарной классификации. В первую очередь визуализируйте соотношение классов в данных:
def count_plot():
    sns.countplot(data=df, x='Revenue')
    plt.show()
#count_plot()

def show_heat_map():
    plt.figure(figsize=(20, 20))
    corr = df_dummies.corr(method='spearman')
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.show()

#show_heat_map()
# По heatmap видимо что нет ярко выраженных признаков по которым можно было бы обучать модель -
# придется обучать по всем - использовать случайный лес, так как
# Суть этого метода заключается в том, что каждая модель обучается не на всех признаках, а только на части из них.
# Такой подход позволяет уменьшить коррелированность между ответами деревьев и сделать их независимыми друг от друга.


#Разделите набор данных на матрицу наблюдений X и вектор ответов y:
X = df_dummies.drop('Revenue', axis=1)
y = df_dummies['Revenue']
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, random_state=42, test_size=0.2, shuffle=True)

december_train = X_train[X_train['Month_Dec'] == True].count()['Month_Dec']
december_test = X_test[X_test['Month_Dec'] == True].count()['Month_Dec']
#убеждаемся, что данные за декабрь попали как в тест, так и в трейн
print(f"Декабрьских сессий в трейне {december_train} и в тесте {december_test}")

#Чему равно количество сессий на сайте в тренировочной выборке?
print(f"всего данных трейн {y_train.count()} тест {y_test.count()}")
