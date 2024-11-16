import requests
import json
import logging

logging.basicConfig(level=logging.INFO)

# 1. Получает все посты пользователя с "userId=5" используя эндпоинт: https://dummyjson.com/users/5/posts.
# 2. Выводит названия постов.


def get_user_posts(user_id):
  logging.info("Отправка запроса на получение списска дел...")
  url = f'https://dummyjson.com/users/{user_id}/posts'
  response = requests.get(url)
  response.raise_for_status()
  return response.json().get('posts')


try:
  for post in get_user_posts(5):
    print(f'\t \u2022 {post.get("title")}')
except Exception as e:
  logging.error(f"Произошла ошибка: {e}")

