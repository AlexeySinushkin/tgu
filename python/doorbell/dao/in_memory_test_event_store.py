import io
import logging
import unittest
from datetime import datetime, timedelta
import pandas as pd

from dao.abstract_event_store import AbstractEventStore
from dao.test_image_dao import load_image
from model.bell_event import BellEvent
from model.image_fs import EventImageFs
from utils.date_utils import get_start_end_pd, date_format


class InMemoryEventStore(AbstractEventStore):
    def __init__(self):
        # создаем фиктивные события
        # смещения во времени - пять часов назад, четыре часа назад и т.д.
        five_hours_ago = datetime.now() - timedelta(hours=5)
        four_hours_ago = datetime.now() - timedelta(hours=4)
        three_hours_ago = datetime.now() - timedelta(hours=3)
        two_hours_ago = datetime.now() - timedelta(hours=2)
        one_hour_ago = datetime.now() - timedelta(hours=1)

        self.events = pd.DataFrame({
            "id": [1, 2, 3, 4, 5],
            "start_date": [five_hours_ago, four_hours_ago, three_hours_ago, two_hours_ago, one_hour_ago],
            # как долго человек находился в зоне действия звонка
            "stop_date": [five_hours_ago + timedelta(minutes=1), four_hours_ago + timedelta(minutes=2),
                          three_hours_ago + timedelta(minutes=3), two_hours_ago + timedelta(minutes=1),
                          one_hour_ago + timedelta(minutes=5)],
        })
        self.images = pd.DataFrame({
            "id": [101, 102, 103, 104, 105, 106, 107],
            # FK
            "event_id": [1, 2, 3, 4, 5, 5, 5],
            "file_name": ["24c72519-900d-4e08-b959-5031fad7334a.png", "e1d79318-9bd2-4806-8b58-e6a0674be86c.png",
            "e89f6261-b3ac-430a-9dc1-f91c53567b3d.png", "ee5c4eeb-fc3a-4eb0-be91-323c8b0984d3.png",
                    "62bf39be-8d8a-41d6-8f1f-6ab7b16e8aeb.png", "26ded303-2786-4f0a-8b45-1eb668b4d24f.png",
                    "69260c41-d496-4958-bbbd-4c74a1a9f3a1.png"]
        })
        pass

    def create(self, image_file_name) -> BellEvent:
        event = BellEvent()
        event.id = self.events["id"].max()+1
        event.start_date = datetime.now()
        event.stop_date = datetime.now()
        self.events = pd.concat([self.events, pd.DataFrame([event.to_map()])], ignore_index=True)

        image = EventImageFs()
        image.id = self.images["id"].max()+1
        image.event_id = event.id
        image.file_name = image_file_name
        self.images = pd.concat([self.images, pd.DataFrame([image.to_map()])], ignore_index=True)
        return event

    def get_event(self, event_id: int) -> BellEvent | None:
        try:
            df = self.events
            record = self.events[df['id']==event_id]
            record = record.iloc[0]
            return self.__from_record(record)
        except Exception as e:
            logging.error(e)
            return None

    def get_events(self, date) -> [BellEvent]:
        df = self.events
        start, end  = get_start_end_pd(date)
        df = self.events[df['start_date'].ge(start) & df['start_date'].le(end)]
        list = []
        for i in range(0, df.shape[0]):
            record = df.iloc[i]
            list.append(self.__from_record(record))
        return list

    def __from_record(self, record):
        bell_event = BellEvent()
        bell_event.id = record['id']
        bell_event.start_date = record['start_date']
        bell_event.stop_date = record['stop_date']
        return bell_event

    def get_images(self, event_id) -> [EventImageFs]:
        df = self.images
        df = df[df['event_id']==event_id]
        return df

    def get_main_image(self, event_id) -> io.BytesIO:
        df = self.images
        df = df[df['event_id'] == event_id]
        file_name = df.iloc[0]["file_name"]
        return load_image(file_name)

    def update(self, event: BellEvent):
        df = self.events
        self.events.loc[df['id'] == event.id, 'stop_date'] = event.stop_date






class TestInMemoryEventStoreCrud(unittest.TestCase):
  def test_create(self):
    store = InMemoryEventStore()
    image = "new-image.png"
    new_event = store.create(image)
    bell_events = store.get_events(datetime.now())
    df = bell_events[bell_events['id']==new_event.id]
    assert df.shape[0] == 1
    attached_image = store.get_images(new_event.id).iloc[0]
    assert image == attached_image.file_name