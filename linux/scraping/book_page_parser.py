# https://books.toscrape.com/catalogue/olio_984/index.html
# Парсит страничку и возвращает объект book

from objects import Book
import requests
from bs4 import BeautifulSoup
import re
import logging


def parse_book(url): # -> book | None
  try:
    response = requests.get(url)
    response.raise_for_status()
    book = Book()
    book.scrape_url = url
    soup = BeautifulSoup(response.text, 'html.parser')
    book_container = soup.find('article', attrs={'class': 'product_page'})
    extra_info_table = book_container.find('table', attrs={'class': 'table-striped'})
    for tr in extra_info_table.findAll('tr'):
      t, v = tr.th.text, tr.td.text
      if t == 'UPC':
        book.upc = v
      elif t == 'Price (excl. tax)':
        book.price_without_tax = parse_price(v)
      elif t == 'Price (incl. tax)':
        book.price_with_tax = parse_price(v)
      elif t == 'Tax':
        book.tax = parse_price(v)
      elif t == 'Availability':
        book.available_count = parse_int(v)
      elif t == 'Number of reviews':
        book.number_of_reviews = parse_int(v)

    name_container = book_container.find('div', attrs={'class': 'product_main'})
    book.name = name_container.h1.text

    price_container = name_container.find('p', attrs={'class': 'price_color'})
    book.price = parse_price(price_container.text)

    rating_container = book_container.find('p', attrs={'class', 'star-rating'})
    book.rating = parse_rating(rating_container.attrs['class'])

    product_description = book_container.find('div', attrs={'id': 'product_description'})
    book.description = product_description.find_next_sibling().text

    return book
  except Exception  as e:
    logging.error(f"Произошла ошибка: {url} {e}")
  return None

def parse_price(money_text): # -> number | None
  result = re.findall(r'[0-9.]+', money_text)
  if len(result)>0:
    return float(result[0])
  return None

def parse_int(money_text): # -> number | None
  result = re.findall(r'[0-9]+', money_text)
  if len(result)>0:
    return int(result[0])
  return None

def parse_rating(rating_css_class):
  for css_class in rating_css_class:
    if css_class == 'One':
      return 1
    elif css_class == 'Two':
      return 2
    elif css_class == 'Three':
      return 3
    elif css_class == 'Four':
      return 4
    elif css_class == 'Five':
      return 5
  return 0