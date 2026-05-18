from app import create_app


def test_user_flow(client):
    response = client.post("/users", json={"name": "vini"})
    assert response.status_code == 201
    user = response.get_json()
    user_id = user["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    response = client.put(f"/users/{user_id}", json={"name": "novo nome"})
    assert response.status_code == 200
    assert response.get_json()["name"] == "novo nome"
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204
    response = client.get(f"/users/{user_id}")
    assert response._status_code == 404


def test_list_users(client):
    client.post("/users", json={"name": "User1"})
    client.post("/users", json={"name": "User2"})
    response = client.get("/users")
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) == 2


def test_full_user_flow_vinicius():
    client = create_app().test_client()
    r = client.post("/users", json={"name": "Vinicius Souza"})
    user_id = r.get_json()["id"]
    assert client.get(f"/users/{user_id}").status_code == 200
    assert (
        client.put(f"/users/{user_id}", json={"name": "Vinicius Leal"}).status_code
        == 200
    )
    assert client.delete(f"/users/{user_id}").status_code == 204


def test_validation_required_name():
    client = create_app().test_client()
    r = client.post("/users", json={})
    assert r.status_code == 400


def test_multiple_users_flow():
    client = create_app().test_client()
    client.post("/users", json={"name": "Paulo Cesar"})
    client.post("/users", json={"name": "João Lima"})
    r = client.get("/users")
    assert len(r.get_json()) == 2
