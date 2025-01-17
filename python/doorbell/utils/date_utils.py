from datetime import datetime, time

import pandas as pd

date_format = "%d.%m.%Y"

def parse_date(date_string: str) -> datetime:
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
    end_of_day = datetime.combine(datetime.now(), time.max)
    return pd.to_datetime(start_of_day), pd.to_datetime(end_of_day)