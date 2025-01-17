from datetime import datetime

class BellEvent:
  id: int
  start_date: datetime
  stop_date:  datetime

  def to_map(self):
      return {"id": self.id, "start_date": self.stop_date, "stop_date": self.stop_date}