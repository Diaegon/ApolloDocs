from http import HTTPStatus

def test_create_projetista_unauthorized(client):
    response = client.post("/projetistas/", json={
        "nome_projetista": "Test Projetista",
        "creci_projetista": "12345",
        "rubrica_projetista": "TP",
        "telefone_projetista": "123456",
        "email_projetista": "projetista@test.com"
    })
    assert response.status_code == HTTPStatus.UNAUTHORIZED

def test_create_projetista_authorized(client, token):
    response = client.post(
        "/projetistas/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome_projetista": "Test Authorized Projetista",
            "creci_projetista": "12345",
            "rubrica_projetista": "TAP",
            "telefone_projetista": "123456",
            "email_projetista": "projetista@test.com"
        }
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["nome_projetista"] == "Test Authorized Projetista"
    assert "id_projetista" in response.json()

def test_read_projetistas(client, token):
    client.post(
        "/projetistas/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome_projetista": "Test Projetista 2",
            "creci_projetista": "12345",
            "rubrica_projetista": "TP2",
            "telefone_projetista": "123456",
            "email_projetista": "projetista@test.com"
        }
    )
    response = client.get("/projetistas/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.OK
    assert "projetistas" in response.json()
    assert len(response.json()["projetistas"]) >= 1

def test_read_projetista_by_id(client, token):
    create_response = client.post(
        "/projetistas/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome_projetista": "Test Projetista 3",
            "creci_projetista": "12345",
            "rubrica_projetista": "TP3",
            "telefone_projetista": "123456",
            "email_projetista": "projetista@test.com"
        }
    )
    obj_id = create_response.json()["id_projetista"]
    
    response = client.get(f"/projetistas/{obj_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.OK
    assert response.json()["id_projetista"] == obj_id

def test_update_projetista(client, token):
    create_response = client.post(
        "/projetistas/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome_projetista": "Test Projetista 4",
            "creci_projetista": "123",
            "rubrica_projetista": "TP4",
            "telefone_projetista": "123",
            "email_projetista": "test@test.com"
        }
    )
    obj_id = create_response.json()["id_projetista"]
    
    response = client.put(
        f"/projetistas/{obj_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome_projetista": "Updated Projetista",
            "creci_projetista": "123",
            "rubrica_projetista": "TP4",
            "telefone_projetista": "123",
            "email_projetista": "test@test.com"
        }
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["nome_projetista"] == "Updated Projetista"

def test_delete_projetista(client, token):
    create_response = client.post(
        "/projetistas/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome_projetista": "Delete me",
            "creci_projetista": "123",
            "rubrica_projetista": "DM",
            "telefone_projetista": "123",
            "email_projetista": "test@test.com"
        }
    )
    obj_id = create_response.json()["id_projetista"]
    
    response = client.delete(f"/projetistas/{obj_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.OK
    
    response = client.get(f"/projetistas/{obj_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.NOT_FOUND
