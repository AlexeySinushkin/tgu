import logging
import csv
from encodings.utf_8 import encode


class BookIterator:
  def __init__(self, book):
    self.book = book
    self.counter = 0

  def __iter__(self):
    self.counter = 0
    return self

  def __next__(self):
    result = None
    if self.counter == 0:
      result = self.book.scrape_url
    elif self.counter == 1:
      result = self.book.upc
    elif self.counter == 2:
      result = self.book.name
    elif self.counter == 3:
      result = self.book.number_of_reviews
    elif self.counter == 4:
      result = self.book.price
    elif self.counter == 5:
      result = self.book.price_with_tax
    elif self.counter == 6:
      result = self.book.price_without_tax
    elif self.counter == 7:
      result = self.book.tax
    elif self.counter == 8:
      result = self.book.rating
    elif self.counter == 9:
      result = self.book.available_count
    elif self.counter == 10:
      result = self.book.description
    else:
      raise StopIteration
    self.counter+=1
    return result

def save_to_csv(books, file_name):
  try:
    logging.info(f'Начало сохранения в файл {file_name}')
    with open(file_name, 'w', newline='', encoding='utf-8') as file:
      writer = csv.writer(file, delimiter=',')
      for book in books:
        logging.info(f'{book.upc} {book.scrape_url}')
        writer.writerow(BookIterator(book))
    logging.info(f'Успешно сохранено {len(books)} записей')
  except Exception as e:
    logging.error(f"Ошибка при сохранении {e}")