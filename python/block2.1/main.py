import cowsay as cw
import logging

logging.basicConfig(level=logging.DEBUG, filename='app.log', encoding='UTF-8', filemode='w', format='%(levelname)s: %(message)s')

logging.info("Программа запущена")
try:
  message = input("Введите сообщение\n")
  cw.cow(message)
except Exception as e: # Добавьте обработку возможных исключений при вводе данных.
  logging.error(f"Произошла ошибка {e}")