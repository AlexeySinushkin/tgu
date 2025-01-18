import unittest
from datetime import datetime, timedelta
from functools import cached_property

import pandas as pd
from pydantic import computed_field
from pydantic.v1 import BaseModel

from model.bell_event import BellEvent

class BellEventDto(BaseModel):
    id: int
    start_date: datetime
    stop_date: datetime
    name: str = ''
    css_class: str = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Инициализация родительского класса User
        delta = self.stop_date - self.start_date
        if delta.seconds>0:
            self.name = "{}   [{} сек]".format(self.start_date.strftime("%X"), delta.seconds)
        else:
            self.name = self.start_date.strftime("%X")




def from_event(event: BellEvent):
    dto = BellEventDto(id = event.id,
                        start_date = event.start_date,
                        stop_date = event.stop_date)
    return dto

def from_dataframe(df: pd.DataFrame)->[BellEventDto]:
    list = []
    for i in range(0, df.shape[0]):
        event = df.iloc[i]
        list.append(BellEventDto(id = event["id"],
                        start_date = event["start_date"],
                        stop_date = event["stop_date"]))
    return list

class BellEventDtoTest(unittest.TestCase):
  def test_create(self):
    event = BellEvent()
    event.id = 21
    event.start_date = datetime.now()
    event.stop_date = datetime.now() + timedelta(seconds=10)
    event_dto = from_event(event)
    print(event_dto)