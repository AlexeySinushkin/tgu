from multiprocessing.connection import default_family

import requests
import json
import logging

from requests import session
from urllib3 import request

logging.basicConfig(level=logging.INFO)

# 1. Авторизуется под пользователем « emilys» с паролем « emilyspass».
# 2. Обновляет поле «lastName» пользователя на «"UpdatedLastName"« с помощью метода «PUT».
# 3. Получает обновленную информацию о пользователе и выводит полное имя.


def auth(auth_data):
  logging.debug("Авторизация...")
  response = requests.post('https://dummyjson.com/auth/login', json=auth_data)
  response.raise_for_status()
  data = response.json()
  return data.get('id'), data.get('accessToken')

def update_last_name(target_user_id, last_name, token):
  logging.debug("Обновление информации...")
  headers = {'Authorization', f'Bearer {token}'}
  json = {'lastName', last_name}
  # Updating a user will not update it into the server.
  # It will simulate a PUT/PATCH request and will return updated user with modified data
  response = requests.put(f'https://dummyjson.com/users/{target_user_id}', headers, json=json)
  response.raise_for_status()

def get_user_info(target_user_id):
  logging.debug("Получение информации о Пользователе...")
  response = requests.get(f'https://dummyjson.com/users/{target_user_id}')
  response.raise_for_status()
  return response.json()


try:
  auth_data = {'username': 'emilys', 'password': 'emilyspass'}
  id, token = auth(auth_data)
  update_last_name(id, 'UpdatedLastName', token)
  user = get_user_info(id)

  if user.get('lastName') == 'UpdatedLastName':
    logging.info('Обновление прошло успешно')
  else:
    logging.error('Фамилия не обновилась на сервере')
except Exception as e:
  logging.error(f"Произошла ошибка: {e}")

