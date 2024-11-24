from book_page_parser import parse_book
from store import save_to_csv

book_url = 'https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html'
# экранизация)) https://youtu.be/ch8SOTvG5dw?list=PL6813019FB9802C52&t=4
book = parse_book(book_url)
assert book.rating == 1
save_to_csv([book], 'test.csv')