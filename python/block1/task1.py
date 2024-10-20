import logging
import csv
from collections import defaultdict
logging.basicConfig(level=logging.DEBUG, filename='app.log', encoding='UTF-8', filemode='w', format='%(levelname)s: %(message)s')


def get_products_from_file(file_name):
  result = list(defaultdict())
  try:
    with open(file_name, "r", encoding='UTF-8') as file:
      reader = csv.DictReader(file, fieldnames=['name', 'amount', 'price'])
      for row in reader:
        item = {"name": row["name"], "amount": int(row["amount"]),
         "price": float(row["price"]) }
        result.append(item)
      logging.info("Данные считаны успешно")
  except ValueError as e:
      logging.error(f"Ошибка формата данных {e}")
  except FileNotFoundError as e:
      logging.error(f"Файл не найден! {e}")
  return result


def pretty_print(products):
  name_max_length = 0
  for product in products:
    name_len = len(product["name"])
    if name_len>name_max_length:
      name_max_length = name_len


  for product in products:
    name = product["name"].ljust(name_max_length, ' ')
    amount = str(product["amount"]).rjust(4, ' ')
    price = str("{:.2f}".format(product["price"])).rjust(10, ' ')
    total = str("{:.2f}".format(product["total"])).rjust(10, ' ')
    print(f"{name} | {amount} | {price} | {total}")


def calculate_total(mut_products):
  total = 0
  for product in mut_products:
    product["total"] = product["amount"] * product["price"]
    total += product["total"]
  return total

products = get_products_from_file("data.txt")
total = calculate_total(products)
pretty_print(products)

# Если общий доход превышает определенное значение,
# выведите сообщение о высоких продажах.
# Где определенные, как определенные не указано.
if total>0:
  print("Высокие продажи!")