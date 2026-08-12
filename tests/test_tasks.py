"""
tests/test_tasks.py
----------------------
Pruebas automáticas del CRUD de tareas, usando pytest + TestClient de FastAPI.

Usamos una base de datos SQLite separada (test.db) solo para pruebas, para
no ensuciar tasks.db, la base de datos real de desarrollo.

Para correr las pruebas:

    pytest -v
"""

import os

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.connection import Base, get_db
from main import app

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def setup_module(module):
    Base.metadata.create_all(bind=engine)


def teardown_module(module):
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("test.db"):
        os.remove("test.db")


def test_create_task():
    response = client.post("/tasks", json={"title": "Estudiar arquitectura"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Estudiar arquitectura"
    assert data["completed"] is False
    assert "id" in data


def test_list_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_get_task():
    created = client.post("/tasks", json={"title": "Tarea de prueba"}).json()
    response = client.get(f"/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_task_not_found():
    response = client.get("/tasks/99999")
    assert response.status_code == 404


def test_update_task():
    created = client.post("/tasks", json={"title": "Tarea a actualizar"}).json()
    response = client.put(f"/tasks/{created['id']}", json={"completed": True})
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_delete_task():
    created = client.post("/tasks", json={"title": "Tarea a borrar"}).json()
    response = client.delete(f"/tasks/{created['id']}")
    assert response.status_code == 204

    response = client.get(f"/tasks/{created['id']}")
    assert response.status_code == 404
