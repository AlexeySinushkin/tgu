from abc import abstractmethod
from collections import defaultdict
from datetime import datetime

import numpy as np

from model.bell_event import BellEvent


class AbstractEventStore:
  @abstractmethod
  def create(self, image) -> BellEvent:
    pass

  @abstractmethod
  def get_last_events(self, limit=100) -> [BellEvent]:
    pass

  @abstractmethod
  def get_image(self, event_id):
    pass



class InMemoryBellEvent:
  def __init__(self, event : BellEvent, image):
    self.event = event
    self.image = image


class InMemoryEventStore(AbstractEventStore):
  counter: int = 1
  events = defaultdict()

  def create(self, image) -> BellEvent:
    event = BellEvent()
    event.id = self.counter
    event.start_date = datetime.now()
    event.stop_date = datetime.now()

    self.events[self.counter] = InMemoryBellEvent(event, image)
    self.counter+=1
    return event

  def get_last_events(self, limit=100):
    map_be = lambda mbe: mbe.event
    return list(map(map_be, self.events.values()))

  def get_image(self, event_id):
    in_mem_event = self.events[event_id]
    return in_mem_event.image


