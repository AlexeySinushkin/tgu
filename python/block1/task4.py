import logging
import csv
from collections import defaultdict
logging.basicConfig(level=logging.DEBUG, filename='app.log', encoding='UTF-8', filemode='w', format='%(levelname)s: %(message)s')

def get_employees_from_file(file_name):
  result = list(defaultdict())
  try:
    with open(file_name, "r", encoding='UTF-8') as file:
      reader = csv.DictReader(file, fieldnames=['name', 'age', 'role', 'salary'])
      for row in reader:
        item = {"name": row["name"], "age": int(row["age"]),
         "role": row["role"], "salary": int(row["salary"]) }
        result.append(item)
      logging.info("Данные считаны успешно")
  except ValueError as e:
      logging.error(f"Ошибка формата данных {e}")
  except FileNotFoundError as e:
      logging.error(f"Файл не найден! {e}")
  return result

def filter_employees(employees):
  if len(employees)>0:
    sum = 0
    for empl in employees:
      sum+=empl["salary"]
    avg = int(sum/len(employees))
    high_earners = list(filter(lambda x: (x["salary"]>avg), employees))
    return high_earners
  return employees

def store_employees(file_name, employees):
  try:
    with open(file_name, "w", encoding='UTF-8') as file:
      for employee in employees:
        empl_info = f"{employee["name"]} - {employee["role"]} - {employee["salary"]}"
        file.write(f"{empl_info}\n")
        print(empl_info)
  except Exception as e:
      logging.error(f"Ошибка при записи файла {e}")

employees = get_employees_from_file("employees.txt")
logging.info(f"Всего сотрудников {len(employees)}")

high_earners = filter_employees(employees)
logging.info(f"Сотрудников с зарплатой выше среднего {len(high_earners)}")
store_employees("high_earners.txt", high_earners)