import cv2
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.responses import StreamingResponse
from starlette.templating import Jinja2Templates

from dao.abstract_event_store import AbstractEventStore
from human_detection_service import EventProducerService
from model.search_area import SearchArea
from utils.date_utils import parse_date, format_date
from dao.in_memory_test_event_store import InMemoryEventStore
from rest_model.bell_event_dto import from_dataframe
from config import settings

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_implementation(test_mode:bool) -> (cv2.VideoCapture, AbstractEventStore):
    if test_mode:
        return cv2.VideoCapture("./test/test_video.mp4"), InMemoryEventStore()
    else:
        return cv2.VideoCapture(settings.get_rtsp_url()), InMemoryEventStore() #TODO sqlite

stream, event_store = get_implementation(settings.test_mode)
#search_area = SearchArea(0.25, 0, 0.85, 0.5)
search_area = SearchArea(0.25, 0, 0.85, 0.9)
service = EventProducerService(stream, search_area, event_store)
service.start()

@app.get("/", response_class=HTMLResponse)
async def last_events(request: Request):
    target_date = request.query_params.get("date")
    target_event_id = request.query_params.get("event_id")
    target_date = parse_date(target_date)

    #по идентификатору события узнаем за какие сутки оно произошло (возможно пользователь вбил руками в адресной строке)
    if target_event_id is not None:
        target_event_id = int(target_event_id)
        bell_event = event_store.get_event(target_event_id)
        if bell_event is not None:
            target_date = bell_event.start_date


    events =  event_store.get_events(target_date)
    events = from_dataframe(events)

    target_event_index = 0
    if target_event_id is not None:
        for i in range(0, len(events)):
            if events[i].id == target_event_id:
                target_event_index=i
                break

    if len(events) == 0:
        return templates.TemplateResponse("dashboard.html", {"request": request, "events": events, "active_event_id": 0, "date": format_date(target_date)})
    else:
        for i in range(0, len(events)):
            if i==target_event_index:
                events[i].css_class = 'btn-primary'
            else:
                events[i].css_class = 'btn-secondary'
        return templates.TemplateResponse("dashboard.html", {"request": request, "events": events, "active_event_id": events[target_event_index].id, "date": format_date(target_date)})



@app.get("/event_main_image/{event_id}",
            response_description="Изображение, послужившее причиной возникновения события",
            response_class=StreamingResponse)
def event_main_image(event_id: int):
    imgio = event_store.get_main_image(event_id)
    return StreamingResponse(content=imgio, media_type="image/png")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)