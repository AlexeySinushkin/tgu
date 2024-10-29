#!/bin/bash
#Задание 5. Объединение файлов (10 баллов)
#У вас есть три текстовых файла: file1.txt, file2.txt и file3.txt. 
#Напишите команду, которая объединит содержимое этих файлов в один новый файл под названием combined.txt.
cat file1.txt > combined.txt && cat file2.txt >> combined.txt && cat file3.txt >> combined.txt
