#!/bin/bash
# --Напишите скрипт, который выводит указанную с клавиатуры строку из файла

# В задаче не сказано принимать номер строки как параметр или запрашивать позже.
# В задаче не сказано принимать название файла как параметр или нет

sed -n $1p 3.txt