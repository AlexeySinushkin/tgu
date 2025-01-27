import logging
import sys

import cv2
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.responses import StreamingResponse
from starlette.templating import Jinja2Templates

from dao.abstract_event_store import AbstractEventStore
from dao.sqlite_event_store import SqLiteEventStore
from human_detection_service import EventProducerService
from model.search_area import SearchArea
from utils.date_utils import parse_date, format_date
from dao.in_memory_test_event_store import InMemoryEventStore
from rest_model.bell_event_dto import from_event
from config import settings

logging.basicConfig(level=logging.INFO, filename='app.log', encoding='UTF-8', filemode='w', format='%(levelname)s: %(message)s')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_implementation(test_mode:bool) -> (cv2.VideoCapture, SearchArea, AbstractEventStore):
    if test_mode:
        return cv2.VideoCapture(settings.test_video_file), settings.search_area, InMemoryEventStore()
    else:
        return cv2.VideoCapture(settings.get_rtsp_url()), settings.search_area, SqLiteEventStore()

stream, search_area, event_store = get_implementation(settings.test_mode)
service = EventProducerService(stream, search_area, event_store)
service.start()

@app.on_event("shutdown")
def shutdown_event():
    service.stop()

@app.get("/", response_class=HTMLResponse)
async def last_events(request: Request):
    target_date = request.query_params.get("date")
    target_event_id = request.query_params.get("event_id")
    logging.debug(f"Запрос на получение событий {target_date}, {target_event_id}")

    target_date = parse_date(target_date)

    #по идентификатору события узнаем за какие сутки оно произошло (возможно пользователь вбил руками в адресной строке)
    if target_event_id is not None:
        target_event_id = int(target_event_id)
        bell_event = event_store.get_event(target_event_id)
        if bell_event is not None:
            target_date = bell_event.start_date


    events = event_store.get_events(target_date)
    events_dto = []
    for e in map(from_event, events):
        events_dto.append(e)

    target_event_index = 0
    if target_event_id is not None:
        for i in range(0, len(events_dto)):
            if events_dto[i].id == target_event_id:
                target_event_index=i
                break

    if len(events_dto) == 0:
        return templates.TemplateResponse("dashboard.html", {"request": request,
                                                             "events": events_dto,
                                                             "active_event_id": 0,
                                                             "date": format_date(target_date)})
    else:
        for i in range(0, len(events_dto)):
            if i==target_event_index:
                events_dto[i].css_class = 'btn-primary'
            else:
                events_dto[i].css_class = 'btn-secondary'
        return templates.TemplateResponse("dashboard.html", {"request": request,
                                                             "events": events_dto,
                                                             "active_event_id": events_dto[target_event_index].id,
                                                             "date": format_date(target_date)})



@app.get("/event_main_image/{event_id}",
            response_description="Изображение, послужившее причиной возникновения события",
            response_class=StreamingResponse)
def event_main_image(event_id: int):
    imgio = event_store.get_main_image(event_id)
    return StreamingResponse(content=imgio, media_type="image/png")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="debug")