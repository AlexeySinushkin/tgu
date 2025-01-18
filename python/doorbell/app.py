

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from utils.date_utils import parse_date, format_date
from dao.in_memory_test_event_store import InMemoryEventStore
from rest_model.bell_event_dto import from_event, from_dataframe

app = FastAPI()
templates = Jinja2Templates(directory="templates")
event_store = InMemoryEventStore()



@app.get("/", response_class=HTMLResponse)
async def last_events(request: Request):
    target_date = request.query_params.get("date")
    target_date = parse_date(target_date)

    events =  event_store.get_events(target_date)
    events = from_dataframe(events)

    target_event_id = request.query_params.get("event_id")
    target_event_index = 0
    if target_event_id is not None:
        target_event_id = int(target_event_id)
        for i in range(0, len(events)):
            if events[i].id == target_event_id:
                target_event_index=i
                break

    if len(events) == 0:
        return templates.TemplateResponse("dashboard.html", {"request": request, "events": events, "active_event_id": 0, "date": format_date(target_date)})
    else:
        events[target_event_index].css_class='active'
        return templates.TemplateResponse("dashboard.html", {"request": request, "events": events, "active_event_id": events[target_event_index].id, "date": format_date(target_date)})



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
    uvicorn.run(app, host="127.0.0.1", port=8001)