import pandas as pd

def print_statistic(csv_file):
  books = pd.read_csv(csv_file)
  print(f'Общее количество {len(books)}')
  if len(books)>0:
    best_books = books[books['rating']==5]
    print(f'Количество книг с максимальной оценкой {len(best_books)}')
    most_expensive_book = books.sort_values(by='price_with_tax', ascending=False)[:1]
    print(f"Самая дорогая книга {most_expensive_book['name'].iloc[0]} c ценой {most_expensive_book['price_with_tax'].iloc[0]}")


# print_statistic('books_data.csv')