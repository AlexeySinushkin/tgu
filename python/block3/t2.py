import requests
import json
import logging

logging.basicConfig(level=logging.INFO)

# 1. Добавляет новый продукт через «https://dummyjson.com/products/add» со следующими данными:
# - Название: «"Test Product"«
# - Описание: «"This is a test product"«
# - Цена: «99»
# 2. Удаляет только что добавленный продукт, используя его «id».
# 3. Подтверждает удаление, пытаясь получить продукт и корректно обрабатывая ошибку.


def create(product):
  logging.debug("Отправка запроса на создание...")
  response = requests.post('https://dummyjson.com/products/add', json=product)
  data = response.json()
  id = data.get('id')
  logging.info(f"Создан объект с id = {id}")
  return id

def delete(id):
  logging.debug("Отправка запроса на удаление...")
  url = f'https://dummyjson.com/products/{id}'
  response = requests.delete(url)
  response.raise_for_status()
  logging.info(f"Удалён объект с id = {id}")

def ensure_object_is_removed(id):
  logging.debug("Попытка получения объекта...")
  url = f'https://dummyjson.com/products/{id}'
  response = requests.head(url)
  if response.status_code == 404:
    logging.info(f"Объект {id} отсутствует на сервере")
    return True
  else:
    logging.error(f"Неожиданный ответ. Возможно ошибка сервера")
    return False

try:
  product = {'title': 'Test Product', 'description': 'This is a test product', 'price': 99}
  id = create(product)
  delete(id)
  if ensure_object_is_removed(id):
    print("Объект был удален")
except Exception as e:
  logging.error(f"Произошла ошибка: {e}")

