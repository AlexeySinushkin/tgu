# path="file_to_convert.csv"
#
# reader = list(csv.reader(open(path, "rU"), delimiter=','))
# writer = csv.writer(open(path, 'w'), delimiter=';')
# writer.writerows(row for row in reader)

import book_page_parser
from book_page_parser import parse_book

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parse_book('https://books.toscrape.com/catalogue/olio_984/index.html')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
