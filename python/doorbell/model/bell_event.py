from datetime import datetime

from pydantic import BaseModel

class BellEvent(BaseModel):
  id: int
  start_date: datetime
  stop_date:  datetime