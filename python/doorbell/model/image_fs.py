
class EventImageFs:
  id: int
  event_id: int
  file_name:  str

  def to_map(self):
      return {"id": self.id, "event_id": self.event_id, "file_name": self.file_name}

