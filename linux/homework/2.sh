#!/bin/bash
result=$(($1%2))
if [ $result = 0 ]; then
echo "Чётное"
else
echo "Нечётное"
fi

