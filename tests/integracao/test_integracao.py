import pytest
from app import create_app
from app.services import user_service


@pytest.fixture
def client():
    app = create_app()

    user_service.users.clear()
    user_service.current_id = 1

    return app.test_client()


def test_create_and_get_user(client):
    created = client.post("/users", json={"name": "vini"})

    assert created.status_code == 201

    user_id = created.get_json()["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.get_json()["name"] == "vini"


def test_create_and_update_user(client):
    created = client.post("/users", json={"name": "paulo"})

    user_id = created.get_json()["id"]

    response = client.put(f"/users/{user_id}", json={"name": "paulo cesar candiani"})

    assert response.status_code == 200
    assert response.get_json()["name"] == "paulo cesar candiani"


def test_create_and_delete_user(client):
    created = client.post("/users", json={"name": "joao"})

    user_id = created.get_json()["id"]

    deleted = client.delete(f"/users/{user_id}")

    assert deleted.status_code == 204

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 404


def test_duplicate_user_integration(client):
    client.post("/users", json={"name": "leal"})

    response = client.post("/users", json={"name": "leal"})

    assert response.status_code == 400


def test_update_nonexistent_user(client):
    response = client.put("/users/999", json={"name": "Teste"})

    assert response.status_code == 404


### NOVOS TESTES DE INTEGRAÇÃO
def test_create_and_get_user_vinicius(client):
    r = client.post("/users", json={"name": "Vinicius Souza"})
    user_id = r.get_json()["id"]

    r = client.get(f"/users/{user_id}")
    assert r.status_code == 200


def test_create_and_update_user_paulo(client):
    r = client.post("/users", json={"name": "Paulo Cesar"})
    user_id = r.get_json()["id"]

    r = client.put(f"/users/{user_id}", json={"name": "Paulo Cesar Atualizado"})
    assert r.get_json()["name"] == "Paulo Cesar Atualizado"


def test_create_and_delete_user_joao(client):
    r = client.post("/users", json={"name": "João Lima"})
    user_id = r.get_json()["id"]

    client.delete(f"/users/{user_id}")
    r = client.get(f"/users/{user_id}")

    assert r.status_code == 404


def test_duplicate_user_integration(client):
    client.post("/users", json={"name": "Vinicius Leal"})
    r = client.post("/users", json={"name": "Vinicius Leal"})
    assert r.status_code == 400


def test_list_users_integration(client):
    client.post("/users", json={"name": "Vinicius Souza"})
    client.post("/users", json={"name": "Paulo Cesar"})

    r = client.get("/users")
    assert len(r.get_json()) == 2