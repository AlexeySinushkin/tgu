from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from dao.abstract_event_store import AbstractEventStore
from model.bell_event import BellEvent
from model.image import EventImage
from utils.date_utils import get_start_end_pd


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

        image = EventImage()
        image.id = self.images["id"].max()+1
        image.event_id = event.id
        image.file_name = image_file_name
        self.images = pd.concat([self.images, pd.DataFrame([image.to_map()])], ignore_index=True)
        return event

    def get_events(self, date) -> [BellEvent]:
        df = self.events
        start, end  = get_start_end_pd(date)
        return self.events[df['start_date'].ge(start) & df['start_date'].le(end)]

    def get_images(self, event_id) -> [EventImage]:
        df = self.images
        df = df[df['event_id']==event_id]
        return df
