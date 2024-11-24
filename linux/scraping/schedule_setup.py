# https://www.geeksforgeeks.org/python-schedule-library/
import schedule
import time
from main import scrape
import logging

def scheduled_scrape():
  logging.info('Скрейпинг начат по расписанию')
  # TODO переименовать текущий файл во избежания конфликтов
  scrape()

schedule.every().day.at("19:00").do(scheduled_scrape)
while True:
  schedule.run_pending()
  time.sleep(1)