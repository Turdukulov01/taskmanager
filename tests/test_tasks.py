def test_create_and_get_task(client):
    # create
    resp = client.post("/tasks", json={"title": "Task A", "description": "desc"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Task A"
    assert data["description"] == "desc"
    assert data["status"] == "created"
    task_id = data["id"]

    # get
    r2 = client.get(f"/tasks/{task_id}")
    assert r2.status_code == 200
    assert r2.json()["id"] == task_id


def test_list_with_filters_and_pagination(client):
    for i in range(5):
        client.post("/tasks", json={"title": f"T{i}", "description": None})

    # список без фильтра, лимит 3
    r = client.get("/tasks", params={"limit": 3, "offset": 0})
    assert r.status_code == 200
    assert len(r.json()) == 3

    # обновим статус одной задачи и проверим фильтр
    t = client.get("/tasks").json()[0]
    client.patch(f"/tasks/{t['id']}", json={"status": "in_progress"})

    r2 = client.get("/tasks", params={"status": "in_progress"})
    assert r2.status_code == 200
    body = r2.json()
    assert len(body) == 1
    assert body[0]["status"] == "in_progress"


def test_update_task(client):
    t = client.post("/tasks", json={"title": "Old", "description": None}).json()
    tid = t["id"]

    r = client.patch(f"/tasks/{tid}", json={"title": "New", "description": "d", "status": "completed"})
    assert r.status_code == 200
    updated = r.json()
    assert updated["title"] == "New"
    assert updated["description"] == "d"
    assert updated["status"] == "completed"


def test_delete_task(client):
    t = client.post("/tasks", json={"title": "ToDel", "description": None}).json()
    tid = t["id"]

    r = client.delete(f"/tasks/{tid}")
    assert r.status_code == 204

    r2 = client.get(f"/tasks/{tid}")
    assert r2.status_code == 404


def test_validation_errors(client):
    # пустой title
    r = client.post("/tasks", json={"title": "", "description": None})
    assert r.status_code == 422

    # неверный статус в update
    t = client.post("/tasks", json={"title": "OK", "description": None}).json()
    r2 = client.patch(f"/tasks/{t['id']}", json={"status": "not_a_status"})
    assert r2.status_code == 422


def test_not_found_update_delete(client):
    r1 = client.patch("/tasks/00000000-0000-0000-0000-000000000000", json={"title": "x"})
    assert r1.status_code == 404

    r2 = client.delete("/tasks/00000000-0000-0000-0000-000000000000")
    assert r2.status_code == 404
