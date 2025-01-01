from pydantic.v1 import BaseModel

from model.bell_event import BellEvent

class BellEventDto(BaseModel):
    id: int
    name: str
    active: str

def from_event(event: BellEvent):
    dto = BellEventDto()
    dto.id=event.id
    dto.name=event.start_date.strftime("%X")
    dto.active = ''
    return dto
