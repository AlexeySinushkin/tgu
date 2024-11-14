import requests
# pycharm ругается на ненужный импорт
import json
import logging

logging.basicConfig(level=logging.INFO)

# Напишите скрипт на Python, который:
# 1. Получает список продуктов с «https://dummyjson.com/products», ограничивая результаты до 10 продуктов на страницу
# и пропуская первые 10 продуктов (т.е., получает вторую страницу).
# 2. Сортирует продукты по цене в порядке убывания.
# 3. Выводит названия продуктов и их цены.
# Добавьте комментарии к каждой строке кода для ясности.))

# создаем функцию
def get_products(params):
  try:
    # Пишем в лог
    logging.info("Отправка запроса к API...")
    # Выполняем запрос
    response = requests.get('https://dummyjson.com/products', params)
    # Преобразуем в map
    data = response.json()
    # берем массив из поля products
    products = data.get('products', [])
    # обходим массив
    for product in products:
      # выводим в консоль (Название функции не соответствует ее поведению)
      print(f"- {product['title']}: ${product['price']}")
    # ловим любые исключения
  except Exception as e:
    # пишем в консоль сообщение с текстом ошибки
    print(f"Произошла ошибка: {e}")

# параметры запроса
params = {
# ограничиваем количество получемых данных
  'limit': 10,
# смещаемся на одну страницу
  'skip': 10,
# просим сервер отсортировать данные по цене
  'sort': 'price',
# по убыванию
  'order': 'desc'
}
# вызываем функцию
get_products(params)