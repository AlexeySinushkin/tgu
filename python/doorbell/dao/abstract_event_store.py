import io
from abc import abstractmethod

from model.bell_event import BellEvent


class AbstractEventStore:
  @abstractmethod
  def create(self, image_file_relative_path) -> BellEvent:
    pass

  @abstractmethod
  def get_event(self, event_id: str) -> BellEvent | None:
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

  #обновляем правую дату (раширяем диапазон присутствия)
  @abstractmethod
  def update(self, event: BellEvent):
    pass

