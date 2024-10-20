import logging
from collections import defaultdict

logging.basicConfig(level=logging.DEBUG, filename='app.log', encoding='UTF-8', filemode='w', format='%(levelname)s: %(message)s')


def get_students_from_file(file_name):
  result = list(defaultdict())
  try:
    with open(file_name, "r", encoding='UTF-8') as file:
      line = file.readline()
      while line:
        name_and_ratings = line.strip().split(",")
        ratings = []
        ratings_count = len(name_and_ratings) - 1
        for i in range(0, ratings_count):
          ratings.append(int(name_and_ratings[i+1]))
        item = {"name": name_and_ratings[0], "ratings" : ratings}
        result.append(item)
        line = file.readline()
      logging.info("Данные считаны успешно")
  except ValueError | TypeError as e:
      logging.error(f"Ошибка формата данных {e}")
  except FileNotFoundError as e:
      logging.error(f"Файл не найден! {e}")
  return result


def calculate_average_rating(student):
  rating_sum = 0
  if len(student["ratings"])>0:
    for rating in student["ratings"]:
      rating_sum+=rating
    return rating_sum/len(student["ratings"])
  return 0

students = get_students_from_file("students.txt")

# - Определите студентов, у которых средний балл выше определенного порога.
good_students = []
for student in students:
  student["avg_rating"] = calculate_average_rating(student)
  if student["avg_rating"]>2:
    good_students.append(student)
    
# Запишите результаты в новый текстовый файл `top_students.txt`.
try:
  with open("top_students.txt", "w", encoding='UTF-8') as file:
    file.write("Ниже приведены студенты у которых средний балл"+
               " выше определенного порога.\n")
    for student in good_students:
      file.write(f"{student["name"]}\n")
except Exception as e:
  logging.error(f"Ошибка при сохранении {e}")

# Выведите информацию о каждом студенте в читабельном формате.
# Какую информацию и что такое читаебльный формат непонятно
for student in students:
  print(f"{student["name"]} - Средний балл {student["avg_rating"]}")