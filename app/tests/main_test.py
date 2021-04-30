from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def tets_read_word():
    response = client.get('/words')
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "something",
        "definition": "somedef",
        "example": "someex",
        "learned": True,
        "times_seen": 1,
        "lang_id": 1
    }

