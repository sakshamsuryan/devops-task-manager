import json
from app import db
from app.models import User

def login(client):
    client.post("/auth/register", data={"name":"Test User","email":"user@example.com","password":"password123"}, follow_redirects=True)

def test_health(client):
    assert client.get("/health").status_code == 200

def test_register_login_and_task_crud(client):
    login(client)
    created = client.post("/api/tasks", json={"title":"Write capstone","priority":"high"})
    assert created.status_code == 201
    task_id = created.get_json()["id"]
    assert client.get("/api/tasks").get_json()[0]["title"] == "Write capstone"
    updated = client.patch(f"/api/tasks/{task_id}", json={"status":"done"})
    assert updated.status_code == 200 and updated.get_json()["status"] == "done"
    assert client.delete(f"/api/tasks/{task_id}").status_code == 200
    assert client.get("/api/tasks").get_json() == []

def test_validation_and_auth(client):
    assert client.get("/api/tasks").status_code == 401 or client.get("/api/tasks").status_code == 302
    login(client)
    assert client.post("/api/tasks", json={"title":""}).status_code == 400
    assert client.post("/api/tasks", json={"title":"bad","status":"unknown"}).status_code == 400

def test_user_cannot_access_other_users_task(client, app):
    login(client)
    task = client.post("/api/tasks", json={"title":"Private task"}).get_json()
    client.post("/auth/logout")
    client.post("/auth/register", data={"name":"Second User","email":"second@example.com","password":"password123"})
    assert client.get(f"/api/tasks/{task['id']}").status_code == 404
