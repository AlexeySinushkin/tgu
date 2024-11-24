from ppretty import ppretty

class Book:
  def __init__(self):
    self.scrape_url = ''
    self.upc = ''
    self.name = ''
    self.description = ''
    self.price = 0.0
    self.price_with_tax = 0.0
    self.price_without_tax = 0.0
    self.tax = 0.0
    self.rating = 0
    self.available_count = 0
    self.number_of_reviews = 0

  # для pandas
  def __getitem__(self, key):
    return getattr(self, key)

  def to_string(self):
    return ppretty(self, seq_length=10)