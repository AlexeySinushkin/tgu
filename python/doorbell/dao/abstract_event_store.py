import io
from abc import abstractmethod

from model.bell_event import BellEvent


class AbstractEventStore:
  @abstractmethod
  def create(self, image) -> BellEvent:
    pass

  @abstractmethod
  def get_events(self, date) -> [BellEvent]:
    pass

  @abstractmethod
  def get_images(self, event_id):
    pass

  @abstractmethod
  def get_main_image(self, event_id) -> io.BytesIO:
    pass
