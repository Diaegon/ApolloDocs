from http import HTTPStatus

def test_create_cliente_unauthorized(client):
    response = client.post("/clientes/", json={
        "nome_cliente": "Test Unauthorized",
        "cpf": "123",
        "data_nascimento": "01/01/2000",
        "rg": "123",
        "telefone_cliente": "123",
        "email_cliente": "test@test.com"
    })
    assert response.status_code == HTTPStatus.UNAUTHORIZED

def test_create_cliente_authorized(client, token):
    response = client.post(
        "/clientes/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome_cliente": "Test Authorized", 
            "cpf": "123456", 
            "data_nascimento": "01/01/2000", 
            "rg": "123456", 
            "telefone_cliente": "123456", 
            "email_cliente": "test2@test.com", 
            "razao_social": None, 
            "nome_fantasia": None, 
            "cnpj": None
        }
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["nome_cliente"] == "Test Authorized"
    assert "id_cliente" in response.json()

def test_read_clientes(client, token):
    client.post(
        "/clientes/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome_cliente": "Test Authorized", 
            "cpf": "123456", 
            "data_nascimento": "01/01/2000", 
            "rg": "123456", 
            "telefone_cliente": "123456", 
            "email_cliente": "test2@test.com", 
            "razao_social": None, 
            "nome_fantasia": None, 
            "cnpj": None
        }
    )
    response = client.get("/clientes/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.OK
    assert "clientes" in response.json()
    assert len(response.json()["clientes"]) >= 1
