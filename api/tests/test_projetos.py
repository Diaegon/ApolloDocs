from http import HTTPStatus

def test_create_projeto_unauthorized(client):
    response = client.post("/projetos/", json={
        "cliente_id": 1,
        "procurador_id": 1,
        "projetista_id": 1
    })
    assert response.status_code == HTTPStatus.UNAUTHORIZED

def _create_dependencies(client, token):
    # Create Cliente
    res_cli = client.post(
        "/clientes/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome_cliente": "Cliente Teste", 
            "cpf": "123456", 
            "data_nascimento": "01/01/2000", 
            "rg": "123456", 
            "telefone_cliente": "123456", 
            "email_cliente": "cliente@test.com", 
            "razao_social": None, 
            "nome_fantasia": None, 
            "cnpj": None
        }
    )
    cliente_id = res_cli.json()["id_cliente"]

    # Create Procurador
    res_proc = client.post(
        "/procuradores/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome_procurador": "Procurador Teste",
            "cpf_procurador": "123456",
            "rg_procurador": "123456",
            "telefone_procurador": "123456",
            "email_procurador": "procurador@test.com",
            "logradouro_procurador": "Rua A",
            "numero_casa_procurador": "1",
            "cep_procurador": "12345-678",
            "bairro_procurador": "Bairro B",
            "cidade_procurador": "Cidade C",
            "estado_procurador": "UF"
        }
    )
    procurador_id = res_proc.json()["id_procurador"]

    # Create Projetista
    res_proj = client.post(
        "/projetistas/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome_projetista": "Projetista Teste",
            "creci_projetista": "12345",
            "rubrica_projetista": "PT",
            "telefone_projetista": "123456",
            "email_projetista": "projetista@test.com"
        }
    )
    projetista_id = res_proj.json()["id_projetista"]

    return cliente_id, procurador_id, projetista_id


def test_create_projeto_authorized(client, token):
    cliente_id, procurador_id, projetista_id = _create_dependencies(client, token)

    response = client.post(
        "/projetos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "cliente_id": cliente_id,
            "procurador_id": procurador_id,
            "projetista_id": projetista_id
        }
    )
    assert response.status_code == HTTPStatus.CREATED
    assert "id_projeto" in response.json()
    assert response.json()["cliente_id"] == cliente_id
    assert response.json()["procurador_id"] == procurador_id

def test_read_projetos(client, token):
    cliente_id, procurador_id, projetista_id = _create_dependencies(client, token)

    client.post(
        "/projetos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "cliente_id": cliente_id,
            "procurador_id": procurador_id,
            "projetista_id": projetista_id
        }
    )

    response = client.get("/projetos/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.OK
    assert "projetos" in response.json()
    assert len(response.json()["projetos"]) >= 1

def test_read_projeto_by_id(client, token):
    cliente_id, procurador_id, projetista_id = _create_dependencies(client, token)

    create_response = client.post(
        "/projetos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "cliente_id": cliente_id,
            "procurador_id": procurador_id,
            "projetista_id": projetista_id
        }
    )
    obj_id = create_response.json()["id_projeto"]

    response = client.get(f"/projetos/{obj_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.OK
    assert response.json()["id_projeto"] == obj_id

def test_update_projeto(client, token):
    cliente_id, procurador_id, projetista_id = _create_dependencies(client, token)

    create_response = client.post(
        "/projetos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "cliente_id": cliente_id,
            "procurador_id": procurador_id,
            "projetista_id": projetista_id
        }
    )
    obj_id = create_response.json()["id_projeto"]

    # Now update by adding an inversor id (which is optional and can be mocked or we can just send the same payload)
    response = client.put(
        f"/projetos/{obj_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "cliente_id": cliente_id,
            "procurador_id": procurador_id,
            "projetista_id": projetista_id,
            "inversor_1_id": 999  # Should work because relations not checked in update schema unless _validate_relations checks inver... Wait, router checks:
        }
    )
    # The _validate_relations only checks cliente, procurador, projetista for valid relation if provided.
    assert response.status_code == HTTPStatus.OK
    assert response.json()["inversor_1_id"] == 999

def test_delete_projeto(client, token):
    cliente_id, procurador_id, projetista_id = _create_dependencies(client, token)

    create_response = client.post(
        "/projetos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "cliente_id": cliente_id,
            "procurador_id": procurador_id,
            "projetista_id": projetista_id
        }
    )
    obj_id = create_response.json()["id_projeto"]

    response = client.delete(f"/projetos/{obj_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.OK

    response = client.get(f"/projetos/{obj_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.NOT_FOUND
