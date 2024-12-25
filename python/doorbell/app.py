from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from model.bell_event import BellEvent

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    data = [
        {"id": "1,001", "column1": "random", "column2": "data", "column3": "placeholder", "column4": "text"},
        {"id": "1,002", "column1": "placeholder", "column2": "irrelevant", "column3": "visual", "column4": "layout"},
        # Добавьте больше строк по необходимости
    ]
    return templates.TemplateResponse("dashboard.html", {"request": request, "data": data})


@app.get("/bell_events/last_day")
def get_bell_events():
  return []