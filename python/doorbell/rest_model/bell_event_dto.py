import unittest
from datetime import datetime

import pandas as pd
from pydantic.v1 import BaseModel

from model.bell_event import BellEvent

class BellEventDto(BaseModel):
    id: int
    name: str
    css_class: str

def from_event(event: BellEvent):
    dto = BellEventDto(id = event.id,
                        name = event.start_date.strftime("%X"),
                        css_class='')
    return dto

def from_dataframe(df: pd.DataFrame)->[BellEventDto]:
    list = []
    for i in range(0, df.shape[0]):
        event = df.iloc[i]
        list.append(BellEventDto(id = event["id"],
                        name = event["start_date"].strftime("%X"),
                        css_class=''))
    return list

class BellEventDtoTest(unittest.TestCase):
  def test_create(self):
    event = BellEvent()
    event.id = 21
    event.start_date = datetime.now()
    event.stop_date = datetime.now()
    event_dto = from_event(event)