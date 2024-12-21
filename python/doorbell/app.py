from fastapi import FastAPI

from model.bell_event import BellEvent

app = FastAPI()

@app.get("/")
def read_root():
  return "Please use /docs address "

@app.get("/bell_events/last_day")
def get_bell_events():
  return []