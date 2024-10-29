#!/bin/bash
# Задание 4. Чистка корзины (5 баллов)
# Напишите скрипт, который находит и удаляет все файлы старше 5 дней в указанной директории.

# Заголовок противоречит описанию задачи По заголовку приходим к выводу, что надо чистить корзину
# По описанию приходим к выводу что надоч истить директорию
# Ниже реализована "Чистка корзины"

target_dir=$1
now_timestamp=`date +%s`
echo Now timestamp is $now_timestamp
delta=$(( 5*24*60*60 ))
threshold=$(( $now_timestamp-$delta ))

IFS=$'\n'
for file_name in $(ls ~/.local/share/Trash/files);
do
info_file_name=~/.local/share/Trash/info/$file_name.trashinfo;
echo $info_file_name
del_date=$(cat $info_file_name | grep DeletionDate= | grep -Po '\d{4}-\d{2}-\d{2}')
timestamp=`date -d"$del_date" +%s`
echo $timestamp
if [[ $timestamp -le $threshold ]]; then
mv ~/.local/share/Trash/files/$file_name $target_dir/
fi
done
