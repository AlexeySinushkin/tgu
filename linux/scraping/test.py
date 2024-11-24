from objects import Book
from store import save_to_csv

book = Book()
book.upc = '123'
book.scrape_url = 'scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html'
save_to_csv([book], 'test.csv')