import logging
import csv
# path="file_to_convert.csv"
#
# reader = list(csv.reader(open(path, "rU"), delimiter=','))
# writer = csv.writer(open(path, 'w'), delimiter=';')
# writer.writerows(row for row in reader)

def save_to_csv(books, file_name):
  try:
    logging.info(f'Начало сохранения в файл {file_name}')
    with open(file_name, 'w') as file:
      writer = csv.writer(file, delimiter=',')
      for book in books:
        writer.writerow(book)
    logging.info(f'Успешно сохранено {len(books)} записей')
  except Exception as e:
    logging.error(f"Ошибка при сохранении {e}")