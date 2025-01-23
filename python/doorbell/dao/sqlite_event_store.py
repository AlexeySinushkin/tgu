import io
import logging
import sqlite3
import unittest
from datetime import datetime


from dao.abstract_event_store import AbstractEventStore
from dao.test_image_dao import load_image
from model.bell_event import BellEvent
from model.image_fs import EventImageFs
from utils.date_utils import get_start_end_pd, format_for_sqlite, parse_sqlite

DEFAULT_DB_NAME = "events.db"

class SqLiteEventStore(AbstractEventStore):
    def __init__(self, db_file_name = DEFAULT_DB_NAME):
        self.db_file_name = db_file_name
        conn = sqlite3.connect(self.db_file_name)
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_date DATE NOT NULL,
            stop_date DATE NOT NULL
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER REFERENCES events(id),
            file_name TEXT NOT NULL,
            creation_date DATE NOT NULL
        )
        """)
        conn.commit()
        conn.close()
        pass

    def create(self, image_file_relative_path) -> BellEvent:
        conn = sqlite3.connect(self.db_file_name)
        cursor = conn.cursor()
        cursor = cursor.execute("INSERT INTO events (start_date, stop_date) VALUES (?, ?)", (datetime.now(), datetime.now()))
        event_id = cursor.lastrowid

        cursor.execute("INSERT INTO images (event_id, file_name, creation_date) VALUES (?, ?, ?)",
                       (event_id, image_file_relative_path, datetime.now()))
        conn.commit()
        conn.close()

        return self.get_event(event_id)

    def get_event(self, event_id: int) -> BellEvent | None:
        try:
            conn = sqlite3.connect(self.db_file_name)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                return self.__row_to_event(row)
        except Exception as e:
            logging.error(e)
            return None

    def get_events(self, date) -> [BellEvent]:
        start, end  = get_start_end_pd(date)
        start = format_for_sqlite(start)
        end = format_for_sqlite(end)
        conn = sqlite3.connect(self.db_file_name)
        cursor = conn.cursor()
        cursor = cursor.execute("SELECT * FROM events WHERE start_date >= ? and start_date <= ?", (start, end,))
        result = []
        for row in cursor.fetchall():
            result.append(self.__row_to_event(row))
        conn.close()
        return result

    def __row_to_event(self, row) -> BellEvent:
        bell_event = BellEvent()
        bell_event.id = row[0]
        bell_event.start_date = parse_sqlite(row[1])
        bell_event.stop_date = parse_sqlite(row[2])
        return bell_event

    def get_images(self, event_id: int) -> [EventImageFs]:
        conn = sqlite3.connect(self.db_file_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM images WHERE event_id = ?", (event_id,))
        result = []
        for row in cursor.fetchall():
            result.append(self.__row_to_image(row))
        conn.close()
        return result

    def get_main_image(self, event_id: int) -> io.BytesIO:
        image = self.get_main_image_record(event_id)
        return load_image(image.file_name)

    def get_main_image_record(self, event_id: int) -> EventImageFs:
        conn = sqlite3.connect(self.db_file_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM images WHERE event_id = ? order by creation_date limit 1", (event_id,))
        row = cursor.fetchone()
        conn.close()
        return self.__row_to_image(row)


    def __row_to_image(self, row) -> EventImageFs:
        image = EventImageFs()
        image.id = row[0]
        image.event_id = row[1]
        image.file_name = row[2]
        return image

    #TODO добавлять второстепенные картинки
    def update(self, event: BellEvent):
        conn = sqlite3.connect(self.db_file_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE events SET stop_date = ? WHERE id = ?", (event.stop_date, event.id))
        conn.commit()
        conn.close()






class SqliteCrudTest(unittest.TestCase):
  def test_create(self):
    store = SqLiteEventStore(f"test-db-{datetime.now().microsecond}.db")
    image = "new-image.png"
    new_event = store.create(image)
    bell_events = store.get_events(datetime.now())
    assert len(bell_events) == 1
    attached_image = store.get_images(new_event.id)[0]
    assert image == attached_image.file_name
    main_image = store.get_main_image_record(new_event.id)
    assert image == main_image.file_name