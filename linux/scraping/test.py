import requests
from bs4 import BeautifulSoup

def wiki_header(url):
  response = requests.get(url)
  page = BeautifulSoup(response.text, 'html.parser')
  container = page.find('nav', class_='vector-toc-landmark')
  title = container.find('h1')
  print(title)  # => Заголовок статьи

wiki_header('https://en.wikipedia.org/wiki/Operating_system')