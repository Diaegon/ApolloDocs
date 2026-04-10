from http import HTTPStatus
from fastapi.testclient import TestClient

def test_create_valid_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert "id" in data

def test_create_user_username_exists(client, user):
    response = client.post(
        "/users/",
        json={
            "username": user.username,
            "email": "anotheremail@example.com",
            "password": "newpassword123",
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT

def test_create_user_email_exists(client, user):
    response = client.post(
        "/users/",
        json={
            "username": "differentusername",
            "email": user.email,
            "password": "newpassword123",
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT

def test_get_users(client, user):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "users" in data
    assert len(data["users"]) >= 1

def test_update_user_valid(client, user, token):
    response = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "updatedusername",
            "email": "updated@example.com",
            "password": "newpassword123",
        },
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["username"] == "updatedusername"
    assert data["email"] == "updated@example.com"

def test_update_user_forbidden(client, user, token):
    # Trying to update someone else
    response = client.put(
        f"/users/9999",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "updatedusername",
            "email": "updated@example.com",
            "password": "newpassword123",
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN

def test_delete_user_valid(client, user, token):
    response = client.delete(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "User deleted"

def test_delete_user_forbidden(client, user, token):
    response = client.delete(
        f"/users/9999",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
