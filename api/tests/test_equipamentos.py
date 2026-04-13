from http import HTTPStatus

import pytest


# ── Payloads ──────────────────────────────────────────────────────────────────

INVERSOR_PAYLOAD = {
    "marca_inversor": "DEYE",
    "modelo_inversor": "SUN-5K-SG03LP1-EU",
    "potencia_inversor": 5000.0,
    "numero_fases": "monofasico",
    "tipo_de_inversor": "string",
    "numero_mppt": 2,
}

PLACA_PAYLOAD = {
    "marca_placa": "CANADIAN SOLAR",
    "modelo_placa": "CS6R-410H",
    "potencia_placa": 410.0,
    "tipo_celula": "monocrystalino",
    "tensao_pico": 49.3,
    "corrente_curtocircuito": 11.09,
    "tensao_maxima_potencia": 41.8,
    "corrente_maxima_potencia": 9.82,
    "eficiencia_placa": 21.4,
}


# ── Inversor CRUD ─────────────────────────────────────────────────────────────

def test_create_inversor(client, token):
    response = client.post(
        "/equipamentos/inversores/",
        json=INVERSOR_PAYLOAD,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["marca_inversor"] == "DEYE"
    assert data["modelo_inversor"] == "SUN-5K-SG03LP1-EU"
    assert data["potencia_inversor"] == 5000.0
    assert data["numero_fases"] == "monofasico"
    assert data["tipo_de_inversor"] == "string"
    assert data["numero_mppt"] == 2
    assert "id_inversor" in data


def test_create_inversor_unauthorized(client):
    response = client.post("/equipamentos/inversores/", json=INVERSOR_PAYLOAD)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_read_inversores(client, token, inversor):
    response = client.get(
        "/equipamentos/inversores/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "inversores" in data
    assert len(data["inversores"]) >= 1
    assert data["inversores"][0]["marca_inversor"] == inversor.marca_inversor


def test_read_inversor_by_id(client, token, inversor):
    response = client.get(
        f"/equipamentos/inversores/{inversor.id_inversor}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["id_inversor"] == inversor.id_inversor
    assert data["marca_inversor"] == inversor.marca_inversor


def test_read_inversor_not_found(client, token):
    response = client.get(
        "/equipamentos/inversores/99999",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_inversor(client, token, inversor):
    updated = {**INVERSOR_PAYLOAD, "potencia_inversor": 6000.0}
    response = client.put(
        f"/equipamentos/inversores/{inversor.id_inversor}",
        json=updated,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["potencia_inversor"] == 6000.0
    assert response.json()["id_inversor"] == inversor.id_inversor


def test_update_inversor_not_found(client, token):
    response = client.put(
        "/equipamentos/inversores/99999",
        json=INVERSOR_PAYLOAD,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_inversor(client, token, inversor):
    response = client.delete(
        f"/equipamentos/inversores/{inversor.id_inversor}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "Inversor deleted"

    # Confirm it's gone
    response = client.get(
        f"/equipamentos/inversores/{inversor.id_inversor}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_inversor_not_found(client, token):
    response = client.delete(
        "/equipamentos/inversores/99999",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


# ── Placa CRUD ────────────────────────────────────────────────────────────────

def test_create_placa(client, token):
    response = client.post(
        "/equipamentos/placas/",
        json=PLACA_PAYLOAD,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["marca_placa"] == "CANADIAN SOLAR"
    assert data["modelo_placa"] == "CS6R-410H"
    assert data["potencia_placa"] == 410.0
    assert data["tensao_pico"] == 49.3
    assert data["corrente_curtocircuito"] == 11.09
    assert data["tensao_maxima_potencia"] == 41.8
    assert data["corrente_maxima_potencia"] == 9.82
    assert "id_placa" in data


def test_create_placa_unauthorized(client):
    response = client.post("/equipamentos/placas/", json=PLACA_PAYLOAD)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_read_placas(client, token, placa):
    response = client.get(
        "/equipamentos/placas/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "placas" in data
    assert len(data["placas"]) >= 1
    assert data["placas"][0]["marca_placa"] == placa.marca_placa


def test_read_placa_by_id(client, token, placa):
    response = client.get(
        f"/equipamentos/placas/{placa.id_placa}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["id_placa"] == placa.id_placa
    assert data["marca_placa"] == placa.marca_placa


def test_read_placa_not_found(client, token):
    response = client.get(
        "/equipamentos/placas/99999",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_placa(client, token, placa):
    updated = {**PLACA_PAYLOAD, "potencia_placa": 450.0}
    response = client.put(
        f"/equipamentos/placas/{placa.id_placa}",
        json=updated,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["potencia_placa"] == 450.0
    assert response.json()["id_placa"] == placa.id_placa


def test_update_placa_not_found(client, token):
    response = client.put(
        "/equipamentos/placas/99999",
        json=PLACA_PAYLOAD,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_placa(client, token, placa):
    response = client.delete(
        f"/equipamentos/placas/{placa.id_placa}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "Placa deleted"

    # Confirm it's gone
    response = client.get(
        f"/equipamentos/placas/{placa.id_placa}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_placa_not_found(client, token):
    response = client.delete(
        "/equipamentos/placas/99999",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
