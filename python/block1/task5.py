import logging
import re
from collections import defaultdict
logging.basicConfig(level=logging.DEBUG, filename='app.log', encoding='UTF-8', filemode='w', format='%(levelname)s: %(message)s')

def get_synonyms_from_file(file_name):
  result = defaultdict()
  try:
    with open(file_name, "r", encoding='UTF-8') as file:
      line = file.readline()
      while line:
        first = ""
        synonyms = []
        for word in re.findall(r"(\w+)", line.strip()):
          if first=="":
            first=word
            continue
          synonyms.append(word)
        result[first.lower()] = synonyms
        line = file.readline()
  except FileNotFoundError as e:
      logging.error(f"Файл не найден! {e}")
  return result

dict = get_synonyms_from_file("synonyms.txt")
print("По условию задачи синонимами являются только значения справочника.")
print("Ключ не является синонимом значений и искать можно только по ключу...")
print("Можем подобрать синонимы для следующих ключей ")
for key in dict.keys():
  print(f"{key} ")

while True:
  key = input("Введите слово (ключ) по которому желаете получить синонимы либо напечатайте 101 для выхода\n").lower().strip()
  logging.debug(key)
  if key in dict.keys():
    print(f"{key}")
    print("Синонимы")
    synonyms = ""
    num = 1
    for value in dict[key]:
      synonyms += f"{num}. {value}"
      if num<len(dict[key]):
        synonyms += ", "
      num += 1
    print(synonyms)
  elif key=="101":
    exit(0)
  else:
    print("Не можем подобрать синонима для этого слова.")