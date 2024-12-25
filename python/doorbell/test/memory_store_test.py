import pytest
import numpy as np
from event_store import InMemoryEventStore


#class TestInMemoryEventStoreCrud(unittest.TestCase):
def test_create():
  store = InMemoryEventStore()
  image = np.array([1, 2, 3])
  event = store.create(image)
  bell_events = store.get_last_events()
  assert 1 == len(bell_events)
  image2 = store.get_image(event.id)
  assert image[0] == image2[0]

def test_limit():
  store = InMemoryEventStore()
  image = np.array([1, 2, 3])
  event = store.create(image)
  bell_events = store.get_last_events()
  assert 1 == len(bell_events)
  image2 = store.get_image(event.id)
  assert image[0] == image2[0]
