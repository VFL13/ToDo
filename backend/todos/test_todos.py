from starlette.testclient import TestClient

from .routes import todo_router

client = TestClient(todo_router)

todos_ids = []
todo_js = {
  "creator": "Igor",
  "title": "Finish Course JS 6 hours",
  "description": "Complete Vladilen Minin's 6 Hour JavaScript Course",
  "create_date": "2020-09-24T12:05:31.477Z",
  "status": "To Do",
}


def _insert_todo():
    response = client.post("/", json=todo_js)
    response_data = response.json()
    if response_data.get("id_", False):
        todos_ids.append(response_data["id_"])
    return response


def test_add_a_todo():
    response = _insert_todo()
    assert response.status_code == 200, "Not able to ADD a new toto"


def test_get_all_todo():
    response = client.get("/")
    assert response.status_code == 200, "Not able to GET todos"


def test_get_a_todo_by_id():
    if not todos_ids:
        _insert_todo()
    assert bool(todos_ids), "Not able to ADD a new todo to later GET it by ID"

    response = client.get(f"/{todos_ids[0]}")
    assert response.status_code == 200, "Not able to GET todo by ID"


def test_update_a_todo_by_id():
    if not todos_ids:
        _insert_todo()
    assert bool(todos_ids), "Not able to ADD a new todo to later UPDATE on it"

    todo_vasya = dict(todo_js)
    todo_vasya.update({"creator": "Vasya"})

    response = client.put(f"/{todos_ids[0]}", json=todo_vasya)
    assert response.status_code == 200, "Not able to UPDATE todo"


def test_delete_a_todos():
    if not todos_ids:
        _insert_todo()
    assert bool(todos_ids), "Not able to ADD a new todo to later DELETION"

    for index, todo in enumerate(todos_ids):
        response = client.delete(f"/{todo}")
        assert response.status_code == 200, "Not able to DELETE a todo by ID"
        del todos_ids[index]
