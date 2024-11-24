import pandas as pd

index = ['upc', 'name', 'number_of_reviews', 'price', 'rating', 'available_count']

def print_statistic(csv_file):
  books = pd.read_csv(csv_file)
  best_books = books[books['rating']==5]
  print(f'Количество книг с максимальной оценкой {len(best_books)}')



print_statistic('books_data.csv')