import re
from datetime import datetime, time

import pandas as pd

date_format = "%d.%m.%Y"
date_format_sqlite = "%Y-%m-%d %H:%M:%S"


def parse_date(date_string: str | None) -> datetime:
    if date_string is None:
        return datetime.now()
    try:
        return datetime.strptime(date_string, date_format)
    except ValueError:
        return datetime.now()

def format_date(date: datetime) -> str:
    return date.strftime(date_format)

def get_start_end(date: datetime)-> (datetime, datetime):
    start_of_day = datetime.combine(date, time.min)
    end_of_day = datetime.combine(datetime.now(), time.max)
    return start_of_day, end_of_day

def get_start_end_pd(date: datetime)-> (datetime, datetime):
    start_of_day = datetime.combine(date, time.min)
    end_of_day = datetime.combine(date, time.max)
    return pd.to_datetime(start_of_day), pd.to_datetime(end_of_day)


def parse_sqlite(date_string: str) -> datetime:
    #убираем миллисекунды из '2025-01-23 14:40:23.531159'
    date_string = re.sub('\\..+', '', date_string)
    return datetime.strptime(date_string, date_format_sqlite)

def format_for_sqlite(date: datetime) -> str:
    return date.strftime(date_format_sqlite)