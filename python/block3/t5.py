import requests
import json
import logging

logging.basicConfig(level=logging.INFO)

# 1. Получает все дела, которые не выполнены, используя «https://dummyjson.com/todos».
# 2. Подсчитывает и выводит количество невыполненных дел.


def get_todos():
  logging.info("Отправка запроса на получение списска дел...")
  response = requests.get('https://dummyjson.com/todos')
  response.raise_for_status()
  return response.json().get('todos')


try:
  incomplete_count = 0
  for todo in get_todos():
    if not todo.get('completed'):
      incomplete_count += 1
  print(f'Количество незавершенных дел {incomplete_count}')
except Exception as e:
  logging.error(f"Произошла ошибка: {e}")

