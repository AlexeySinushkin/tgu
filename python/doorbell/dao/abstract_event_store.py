from abc import abstractmethod

from model.bell_event import BellEvent


class AbstractEventStore:
  @abstractmethod
  def create(self, image) -> BellEvent:
    pass

  @abstractmethod
  def get_last_events(self, limit=100) -> [BellEvent]:
    pass

  @abstractmethod
  def get_images(self, event_id):
    pass

