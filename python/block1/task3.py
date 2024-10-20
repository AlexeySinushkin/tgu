import logging
import os
from collections import defaultdict

logging.basicConfig(level=logging.DEBUG, filename='app.log', encoding='UTF-8', filemode='w', format='%(levelname)s: %(message)s')

def print_rules():
  print("Пример использования: Напечатайте")
  print("Добавить [Описание задачи] - для добавления задачи")
  print("Удалить 1, где 1 - это номер задачи - для удаления задачи")
  print("Выйти - для выхода из программы")


def print_tasks():
  task_num = 1
  try:
    with open("tasks.txt", "r", encoding='UTF-8') as file:
      line = file.readline()
      while line:
        print(f"{task_num} - {line.strip()}")
        task_num+=1
        line = file.readline()
  except FileNotFoundError as e:
      logging.error(f"Файл не найден! {e}")
  except Exception as e:
      logging.error(f"Ошибка при чтении файла {e}")

def add_task(task):
  try:
    with open("tasks.txt", "a", encoding='UTF-8') as file:
      file.write(f"{task}\n")
      print("Задача добавлена")
  except FileNotFoundError as e:
      logging.error(f"Файл не найден! {e}")
  except Exception as e:
      logging.error(f"Ошибка при чтении файла {e}")

def remove_task(task_num):
  try:
    removed = False
    with (open("tasks.txt", "r", encoding='UTF-8') as file_read,
          open("tasks.txt.new", "w", encoding='UTF-8') as file_write):
      current_num = 1
      line = file_read.readline()
      while line:
        if task_num==current_num:
          removed = True
        else:
          file_write.write(line)
        line = file_read.readline()
        current_num += 1
    if removed:
      print("Задача удалена")
      os.rename("tasks.txt", "tasks.txt.old")
      os.rename("tasks.txt.new", "tasks.txt")
      os.remove("tasks.txt.old")
    else:
      print(f"Задача под номером {task_num} не была найдена")
  except FileNotFoundError as e:
      logging.error(f"Файл не найден! {e}")
  except Exception as e:
      logging.error(f"Ошибка при чтении файла {e}")

print_rules()
add_command_length = len("Добавить ")
remove_command_length = len("Удалить ")
exit_command_length = len("Выйти")
print_tasks()
while True:
  command = input("Введите команду\n").strip()
  if command.startswith("Добавить ") and len(command)>add_command_length:
    add_task(command[add_command_length:len(command)])
    print_tasks()
  elif command.startswith("Удалить ") and len(command)>remove_command_length:
    try:
      task_num = int(command[remove_command_length:len(command)])
      remove_task(task_num)
    except ValueError:
      print("Для удаления задачи введите число")
      print_rules()
    else:
      print_tasks()
  elif command.startswith("Выйти") and len(command) >= exit_command_length:
    break
  else:
    print_rules()
    print_tasks()


