from book_list_page_parser import parse_page
from book_page_parser import parse_book
import logging

from store import save_to_csv

logging.basicConfig(level=logging.INFO)


base_path = 'https://books.toscrape.com/'
pages_count = 2 #10000

# Подразумеваем что страниц в будущем будет не более 10000
# Постранично вычитываем количество книг с каждой страницы
# Если окажется 0 - значит последняя (не существующая страница)
# на данный момент их 50

# на первом этапе все книги держим в ОЗУ. В реальном проекте надо после парсинга каждой
# страницы сохранять в БД и выполнять анализ аггрегирующими запросами SQL
books = {}
for page_num in range(1, pages_count):
    logging.info(f'Начало парсинга списска книг на {page_num} странице ')
    book_links = parse_page(f'{base_path}catalogue/page-{page_num}.html')
    if len(book_links) == 0:
        break
    for book_link in book_links:
        book_link = f'{base_path}catalogue/{book_link}'
        logging.info(f'Начало загрузки книги со страницы {book_link}')
        book = parse_book(book_link)
        if not book is None:
            # Дубликаты убираем с помощью Map
            books[book.upc] = book
            logging.debug(book.to_string())
            book.scrape_url = book_link
        else:
            logging.warning(f'Не удалось загрузить книгу по адресу {book_link}')

# Выведите основные статистики по числовым данным...
print(f'Количество книг {len(books)}')
save_to_csv(books, 'books.csv')