from book_list_page_parser import parse_page
from book_page_parser import parse_book
import logging

from books_stat import print_statistic
from store import save_to_csv

logging.basicConfig(level=logging.INFO)


base_path = 'https://books.toscrape.com/'
file_name = 'books_data.csv'
# Подразумеваем что страниц в будущем будет больше 50
# Постранично вычитываем количество книг с каждой страницы
# Если окажется 0 - значит последняя (не существующая страница)

# на первом этапе все книги держим в ОЗУ. В реальном проекте надо после парсинга каждой
# страницы сохранять в БД и выполнять анализ агрегирующими запросами SQL
def scrape():
    books_map = {}
    page_num = 1
    while True:
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
                books_map[book.upc] = book
                logging.debug(book.to_string())
            else:
                logging.warning(f'Не удалось загрузить книгу по адресу {book_link}')
        page_num+=1

    save_to_csv(books_map.values(), file_name)
    logging.info(f'Завершено успешно. Сохранено {len(books_map)}')
    # Выведите основные статистики по числовым данным...
    print_statistic(file_name)

if __name__ == '__main__':
    scrape()