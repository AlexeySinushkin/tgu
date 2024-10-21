import requests
import logging
import json

# Настройка логирования
logging.basicConfig(level=logging.INFO)

def fetch_data():
    url = "https://httpbin.org/get"
    try:
        response = requests.get(url)
        response.raise_for_status() # Проверка статуса ответа
        data = response.json()
        print(json.dumps(data, indent=4)) # Красивый вывод JSON
        logging.info("Данные успешно получены")
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при выполнении запроса: {e}")

if __name__ == "__main__":
    fetch_data()