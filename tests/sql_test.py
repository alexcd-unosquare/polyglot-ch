from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_word():
    response = client.post(
        "/langs/1/add",
        json={
            "name": "dog",
            "definition": "Animal with four legs, two eyes, one tail",
            "example": "Pluto is a dog",
            "learned": False,
            "times_seen": 0,
            "lang_id": 1
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "dog"
    assert "id" in data
    word_id = data["id"]

    response = client.get(f"/words/{word_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "dog"
    assert data["id"] == word_id
