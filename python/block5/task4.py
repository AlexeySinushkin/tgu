# Реализуйте программу, которая создает DataFrame из словаря, где ключами являются
# названия колонок, а значениями — списки данных.
import pandas as pd
import numpy as np
import datetime

dict1 = {'Колонка1': list([0,1]),'Колонка2': list([2,3])}
df = pd.DataFrame(dict1)
print(df)