import numpy as np #для матричных вычислений
import pandas as pd #для анализа и предобработки данных
import matplotlib.pyplot as plt #для визуализации
import seaborn as sns #для визуализации
from fontTools.ttLib.tables.S_V_G_ import doc_index_entry_format_0Size
from pandas.core.util.numba_ import get_jit_arguments

from sklearn import metrics, preprocessing, linear_model  # метрики
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
# По heatmap видимо что признаки Administrative_Duration, Informational, Informational_Duration, ProductRelated, ProductRelated_Duration -
# коррелируют между собой плюс минус одинаково, что приведет нас к мультиколлинеарности при использовании линейной или пол. регрессии
# Будем использовать Случайный лес
# Суть этого метода заключается в том, что каждая модель обучается не на всех признаках, а только на части из них.
# Такой подход позволяет уменьшить коррелированность между ответами деревьев и сделать их независимыми друг от друга.

# Также видно что некоторые аттрибуты слабо коррелируют по отношению к целевому признаку
# Удаляем те, что ниже 0.02
df_dummies = df_dummies.drop(['OperatingSystems', 'Browser', 'TrafficType', 'Month_Aug', 'Month_Jul', 'VisitorType_Other'], axis=1)

#Разделите набор данных на матрицу наблюдений X и вектор ответов y:
X_orig = df_dummies.drop('Revenue', axis=1)
y_orig = df_dummies['Revenue']
#Перемешивать нужно, иначе в тест попадет больше данных за декабрь, а должно попасть пропорционально меньше
X_train, X_test, y_train, y_test = model_selection.train_test_split(X_orig, y_orig, random_state=42, test_size=0.2, shuffle=True)

december_train = X_train[X_train['Month_Dec'] == True].count()['Month_Dec']
december_test = X_test[X_test['Month_Dec'] == True].count()['Month_Dec']
#убеждаемся, что данные за декабрь попали как в тест, так и в трейн
print(f"Декабрьских сессий в трейне {december_train} и в тесте {december_test}")

#Чему равно количество сессий на сайте в тренировочной выборке?
print(f"всего данных трейн {y_train.count()} тест {y_test.count()}")

#Производим нормализацию данных с помощью min-max нормализации
scaler = preprocessing.MinMaxScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

#Создаем объект класса случайный лес
rf = ensemble.RandomForestClassifier(
    random_state=42
)
#Обучаем модель
rf.fit(X_train, y_train)
#Выводим значения метрики
y_train_pred = rf.predict(X_train)
print('Train: {:.2f}'.format(metrics.f1_score(y_train, y_train_pred)))
y_test_pred = rf.predict(X_test)
print('Test: {:.2f}'.format(metrics.f1_score(y_test, y_test_pred)))


def print_metric(model, X, y, scoring):
    # Создаём объект кросс-валидатора KFold
    kf = model_selection.StratifiedKFold(n_splits=5)
    # Считаем метрики на кросс-валидации k-fold
    cv_metrics = model_selection.cross_validate(
        estimator=model,  # модель
        X=X,  # матрица наблюдений X
        y=y,  # вектор ответов y
        cv=kf,  # кросс-валидатор
        scoring=scoring,  # метрика
        return_train_score=True  # подсчёт метрики на тренировочных фолдах
    )
    #print(cv_metrics)
    print('Train k-fold mean {}: {:.2f}'.format(scoring, np.mean(cv_metrics['train_score'])))
    print('Valid k-fold mean {}: {:.2f}'.format(scoring, np.mean(cv_metrics['test_score'])))

def plot_learning_curve(model, X, y, ax=None, title=""):
    kf = model_selection.StratifiedKFold(n_splits=5)
    train_sizes, train_scores, valid_scores = model_selection.learning_curve(
        estimator=model,  # модель
        X=X,  # матрица наблюдений X
        y=y,  # вектор ответов y
        cv=kf,  # кросс-валидатор
        scoring='f1'  # метрика
    )
    # Вычисляем среднее значение по фолдам для каждого набора данных
    train_scores_mean = np.mean(train_scores, axis=1)
    valid_scores_mean = np.mean(valid_scores, axis=1)
    # Строим кривую обучения по метрикам на тренировочных фолдах
    ax.plot(train_sizes, train_scores_mean, label="Train")
    # Строим кривую обучения по метрикам на валидационных фолдах
    ax.plot(train_sizes, valid_scores_mean, label="Valid")
    # Даём название графику и подписи осям
    ax.set_title("Learning curve: {}".format(title))
    ax.set_xlabel("Train data size")
    ax.set_ylabel("Score")
    # Устанавливаем отметки по оси абсцисс
    ax.xaxis.set_ticks(train_sizes)
    # Устанавливаем диапазон оси ординат
    ax.set_ylim(0, 1)
    # Отображаем легенду
    ax.legend()

rf5 = ensemble.RandomForestClassifier(
    criterion='entropy',
    n_estimators=200,
    max_depth=5,
    min_samples_leaf=5,
    random_state=42
)
rf7 = ensemble.RandomForestClassifier(
    criterion='entropy',
    n_estimators=200,
    max_depth=7,
    min_samples_leaf=5,
    random_state=42
)
rf12 = ensemble.RandomForestClassifier(
    criterion='entropy',
    n_estimators=200,
    max_depth=12,
    min_samples_leaf=5,
    random_state=42
)

#Соотношение целевого признака в train и в test (должно быть примерно одинаковым)
print('Train:\n', y_train.value_counts(normalize=True), sep='')
print('Valid:\n', y_test.value_counts(normalize=True), sep='')

def plot_learning_curves():
    fig, axes = plt.subplots(1, 3, figsize=(15, 4)) #фигура + 3 координатных плоскости
    plot_learning_curve(rf5, X_train_scaled, y_train, ax=axes[0], title='Глубина 5')
    plot_learning_curve(rf7, X_train_scaled, y_train, ax=axes[1], title='Глубина 7')
    plot_learning_curve(rf12, X_train_scaled, y_train, ax=axes[2], title='Глубина 12')
    plt.show()

#plot_learning_curves()
print_metric(rf12, X_train_scaled, y_train, 'accuracy')

#Выводим значения метрики
rf12.fit(X_train_scaled, y_train)
y_test_pred = rf12.predict(X_test_scaled)
print('F1 on test: {:.2f}'.format(metrics.f1_score(y_test, y_test_pred)))
print(metrics.classification_report(y_test, y_test_pred))

#Рассчитайте значение метрики F1 для посетителей, завершивших сессию без покупки товара?
# На предсказание надо подать данные, где есть сессии только лишь без покупки
df_no_revenue = df_dummies.copy()
df_no_revenue = df_no_revenue[df_no_revenue['Revenue'] == False]
print(f"Количество сессий без покупки {df_no_revenue.shape[0]}")
X_no_revenue = df_no_revenue.drop('Revenue', axis=1)
y_no_revenue = df_no_revenue['Revenue']
X_no_revenue_scaled = scaler.transform(X_no_revenue)
y_no_revenue_pred = rf12.predict(X_no_revenue_scaled)
print('F1 no revenue: {:.2f}'.format(metrics.f1_score(y_no_revenue, y_no_revenue_pred)))

df_revenue = df_dummies.copy()
df_revenue = df_revenue[df_revenue['Revenue'] == True]
print(f"Количество сессий завершившихся покупкой {df_revenue.shape[0]}")
X_revenue = df_revenue.drop('Revenue', axis=1)
y_revenue = df_revenue['Revenue']
X_revenue_scaled = scaler.transform(X_revenue)
y_revenue_pred = rf12.predict(X_revenue_scaled)
print('F1 revenue: {:.2f}'.format(metrics.f1_score(y_revenue, y_revenue_pred)))

def print_pr(model, X, y):
    kf = model_selection.StratifiedKFold(n_splits=5)
    # Делаем предсказание вероятностей на кросс-валидации
    y_cv_proba_pred = model_selection.cross_val_predict(model, X, y, cv=kf, method='predict_proba')
    # Выделяем столбец с вероятностями для класса 1
    y_cv_proba_pred = y_cv_proba_pred[:, 1]
    # Вычисляем координаты PR-кривой
    precision, recall, thresholds = metrics.precision_recall_curve(y_train, y_cv_proba_pred)
    print('Thresholds:', thresholds[:5])
    print('Precision scores:', precision[:5])
    print('Recall scores:', recall[:5])

    # Вычисляем F1-меру при различных threshold
    f1_scores = (2 * precision * recall) / (precision + recall)
    # Определяем индекс максимума
    idx = np.argmax(f1_scores)
    print('Best threshold = {:.2f}, F1-Score = {:.2f}'.format(thresholds[idx], f1_scores[idx]))

    # Строим PR-кривую
    fig, ax = plt.subplots(figsize=(10, 5))  # фигура + координатная плоскость
    # Строим линейный график зависимости precision от recall
    ax.plot(recall, precision, label='PR')
    # Отмечаем точку максимума F1
    ax.scatter(recall[idx], precision[idx], marker='o', color='black', label='Best F1 score')
    # Даем графику название и подписи осям
    ax.set_title('Precision-recall curve')
    ax.set_xlabel('Recall')
    ax.set_ylabel('Precision')
    # Отображаем легенду
    ax.legend()

#print_pr(rf12, X_train_scaled, y_train)
#plt.show()

#Задаём оптимальный порог вероятностей
threshold_opt = 0.37
y_test_pred_proba = rf12.predict_proba(X_test_scaled)[:, 1]
y_test_pred = y_test_pred_proba > threshold_opt
#Считаем метрики
print(metrics.classification_report(y_test, y_test_pred))

df_no_revenue = df_dummies.copy()
df_no_revenue = df_no_revenue[df_no_revenue['Revenue'] == False]
print(f"Количество сессий без покупки {df_no_revenue.shape[0]}")
X_no_revenue = df_no_revenue.drop('Revenue', axis=1)
y_no_revenue = df_no_revenue['Revenue']
X_no_revenue_scaled = scaler.transform(X_no_revenue)
y_no_revenue_pred = rf12.predict_proba(X_no_revenue_scaled)[:, 1]
y_no_revenue_pred = y_no_revenue_pred > threshold_opt
print('F1 no revenue: {:.2f}'.format(metrics.f1_score(y_no_revenue, y_no_revenue_pred)))

df_revenue = df_dummies.copy()
df_revenue = df_revenue[df_revenue['Revenue'] == True]
print(f"Количество сессий завершившихся покупкой {df_revenue.shape[0]}")
X_revenue = df_revenue.drop('Revenue', axis=1)
y_revenue = df_revenue['Revenue']
X_revenue_scaled = scaler.transform(X_revenue)
y_revenue_pred = rf12.predict_proba(X_revenue_scaled)[:, 1]
y_revenue_pred = y_revenue_pred > threshold_opt
print('F1 revenue: {:.2f}'.format(metrics.f1_score(y_revenue, y_revenue_pred)))