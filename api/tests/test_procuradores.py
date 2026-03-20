from http import HTTPStatus

def test_create_procurador_unauthorized(client):
    response = client.post("/procuradores/", json={
        "nome_procurador": "Test Unauthorized",
        "cpf_procurador": "123",
        "rg_procurador": "123",
        "telefone_procurador": "123",
        "email_procurador": "test@test.com",
        "logradouro_procurador": "Rua A",
        "numero_casa_procurador": "1",
        "cep_procurador": "12345-678",
        "bairro_procurador": "Bairro B",
        "cidade_procurador": "Cidade C",
        "estado_procurador": "UF"
    })
    assert response.status_code == HTTPStatus.UNAUTHORIZED

def test_create_procurador_authorized(client, token):
    response = client.post(
        "/procuradores/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome_procurador": "Test Authorized",
            "cpf_procurador": "123456",
            "rg_procurador": "123456",
            "telefone_procurador": "123456",
            "email_procurador": "test2@test.com",
            "logradouro_procurador": "Rua A",
            "numero_casa_procurador": "1",
            "complemento_procurador": "Apto 1",
            "cep_procurador": "12345-678",
            "bairro_procurador": "Bairro B",
            "cidade_procurador": "Cidade C",
            "estado_procurador": "UF"
        }
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["nome_procurador"] == "Test Authorized"
    assert "id_procurador" in response.json()

def test_read_procuradores(client, token):
    client.post(
        "/procuradores/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome_procurador": "Test Authorized 2",
            "cpf_procurador": "987",
            "rg_procurador": "987",
            "telefone_procurador": "987",
            "email_procurador": "test3@test.com",
            "logradouro_procurador": "Rua B",
            "numero_casa_procurador": "2",
            "cep_procurador": "12345-678",
            "bairro_procurador": "Bairro C",
            "cidade_procurador": "Cidade D",
            "estado_procurador": "XX"
        }
    )
    response = client.get("/procuradores/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.OK
    assert "procuradores" in response.json()
    assert len(response.json()["procuradores"]) >= 1

def test_read_procurador_by_id(client, token):
    create_response = client.post(
        "/procuradores/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome_procurador": "Test Authorized 3",
            "cpf_procurador": "987",
            "rg_procurador": "987",
            "telefone_procurador": "987",
            "email_procurador": "test3@test.com",
            "logradouro_procurador": "Rua B",
            "numero_casa_procurador": "2",
            "cep_procurador": "12345-678",
            "bairro_procurador": "Bairro C",
            "cidade_procurador": "Cidade D",
            "estado_procurador": "XX"
        }
    )
    obj_id = create_response.json()["id_procurador"]
    
    response = client.get(f"/procuradores/{obj_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.OK
    assert response.json()["id_procurador"] == obj_id

def test_update_procurador(client, token):
    create_response = client.post(
        "/procuradores/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome_procurador": "Test Authorized 4",
            "cpf_procurador": "987",
            "rg_procurador": "987",
            "telefone_procurador": "987",
            "email_procurador": "test@test.com",
            "logradouro_procurador": "Rua",
            "numero_casa_procurador": "1",
            "cep_procurador": "123",
            "bairro_procurador": "B",
            "cidade_procurador": "C",
            "estado_procurador": "E"
        }
    )
    obj_id = create_response.json()["id_procurador"]
    
    response = client.put(
        f"/procuradores/{obj_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome_procurador": "Updated Procurador",
            "cpf_procurador": "987",
            "rg_procurador": "987",
            "telefone_procurador": "987",
            "email_procurador": "test@test.com",
            "logradouro_procurador": "Rua",
            "numero_casa_procurador": "1",
            "cep_procurador": "123",
            "bairro_procurador": "B",
            "cidade_procurador": "C",
            "estado_procurador": "E"
        }
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["nome_procurador"] == "Updated Procurador"

def test_delete_procurador(client, token):
    create_response = client.post(
        "/procuradores/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome_procurador": "Delete me",
            "cpf_procurador": "987",
            "rg_procurador": "987",
            "telefone_procurador": "987",
            "email_procurador": "test@test.com",
            "logradouro_procurador": "Rua",
            "numero_casa_procurador": "1",
            "cep_procurador": "123",
            "bairro_procurador": "B",
            "cidade_procurador": "C",
            "estado_procurador": "E"
        }
    )
    obj_id = create_response.json()["id_procurador"]
    
    response = client.delete(f"/procuradores/{obj_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.OK
    
    response = client.get(f"/procuradores/{obj_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.NOT_FOUND
