

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from utils.date_utils import parse_date, format_date
from dao.abstract_event_store import InMemoryEventStore
from rest_model.bell_event_dto import  from_event

app = FastAPI()
templates = Jinja2Templates(directory="templates")
event_store = InMemoryEventStore()



@app.get("/", response_class=HTMLResponse)
async def last_events(request: Request):
    target_date = parse_date(request.query_params.get("date"))

    events =  event_store.get_events(target_date)
    events = list(map(lambda e: from_event(e), events))

    if len(events) == 0:
        return templates.TemplateResponse("dashboard.html", {"request": request, "events": events, "active_event_id": 0, "date": format_date(target_date)})
    else:
        events[0].active='active'
        return templates.TemplateResponse("dashboard.html", {"request": request, "events": events, "active_event_id": events[0].id, "date": format_date(target_date)})



@app.get("/view_event/{event_id}", response_class=HTMLResponse)
async def view_event(event_id: int):
    if event_id is None:
        events =  event_store.get_last_events()
        if len(events) == 0:
            return templates.TemplateResponse("dashboard.html", {"events": events})
        else:
            return templates.TemplateResponse("dashboard.html", {"events": events, "active_event_id": event_id})
    else:
        #TODO
        events = event_store.get_last_events()
        return templates.TemplateResponse("dashboard.html", {"events": events})

@app.get("/bell_events/last_day")
def get_bell_events():
  return []

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)