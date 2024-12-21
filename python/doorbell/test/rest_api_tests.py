from fastapi.testclient import TestClient

from app import app

client = TestClient(app)
base_path = "http://127.0.0.1:8000"

def test_get_bell_events():
  response = client.get(f"{base_path}/bell_events/last_day")
  assert response.status_code == 200
  assert response.json() == []