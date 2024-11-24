# https://books.toscrape.com/catalogue/page-3.html
# Парсит страничку со списском книг и возвращает список ссылок

import requests
from bs4 import BeautifulSoup


def parse_page(url): # -> string[]
  result = []
  try:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for article in soup.find_all('article', attrs={'class': 'product_pod'}):
      book_url = article.h3.a.attrs['href']
      if not (book_url is None):
        result.append(book_url)
  except Exception  as e:
    print(e)
  return result

