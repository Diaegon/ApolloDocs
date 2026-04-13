"""
Tests for document generation endpoints in /docs.

Strategy:
- Each test authenticates as a valid user, submits a standard payload,
  and asserts the response is a downloadable PDF file.
- No assertions are made about document content, only about delivery.
"""

import zipfile
from http import HTTPStatus
from io import BytesIO

from api.tests.test_payloads import (
    COMPLETO_PAYLOAD,
    FORMULARIO_PAYLOAD,
    MEMORIAL_PAYLOAD,
    MEMORIAL_V2_BASE,
    PROCURACAO_PAYLOAD,
    UNIFILAR_PAYLOAD,
    UNIFILAR_V2_BASE,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _assert_pdf_response(response):
    """Verify the response delivers a downloadable PDF."""
    # StreamingResponse in FastAPI always returns 200 regardless of the
    # router's status_code declaration, so we accept both 200 and 201.
    assert response.status_code in {HTTPStatus.OK, HTTPStatus.CREATED}
    assert response.headers["content-type"] == "application/pdf"
    assert "attachment" in response.headers.get("content-disposition", "")
    assert len(response.content) > 0, "PDF content should not be empty"


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_generate_memorial_descritivo(client, user, token):
    """POST /docs/memorialdescritivo should return a downloadable PDF."""
    response = client.post(
        "/docs/memorialdescritivo",
        json=MEMORIAL_PAYLOAD,
        headers={"Authorization": f"Bearer {token}"},
    )
    _assert_pdf_response(response)


def test_generate_procuracao(client, user, token):
    """POST /docs/procuracao should return a downloadable PDF."""
    response = client.post(
        "/docs/procuracao",
        json=PROCURACAO_PAYLOAD,
        headers={"Authorization": f"Bearer {token}"},
    )
    _assert_pdf_response(response)


def test_generate_diagrama_unifilar(client, user, token):
    """POST /docs/diagramaunifilar should return a downloadable PDF."""
    response = client.post(
        "/docs/diagramaunifilar",
        json=UNIFILAR_PAYLOAD,
        headers={"Authorization": f"Bearer {token}"},
    )
    _assert_pdf_response(response)


def test_generate_formulario_enel(client, user, token):
    """POST /docs/formularioenel should return a downloadable PDF."""
    response = client.post(
        "/docs/formularioenel",
        json=FORMULARIO_PAYLOAD,
        headers={"Authorization": f"Bearer {token}"},
    )
    _assert_pdf_response(response)


def test_generate_todos_documentos(client, user, token):
    """POST /docs/todos should return a ZIP archive containing all four PDFs."""
    response = client.post(
        "/docs/todos",
        json=COMPLETO_PAYLOAD,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code in {HTTPStatus.OK, HTTPStatus.CREATED}
    assert response.headers["content-type"] == "application/zip"
    assert "attachment" in response.headers.get("content-disposition", "")
    assert len(response.content) > 0, "ZIP content should not be empty"

    with zipfile.ZipFile(BytesIO(response.content)) as zf:
        names = zf.namelist()
        assert "memorial_descritivo.pdf" in names
        assert "procuracao.pdf" in names
        assert "diagrama_unifilar.pdf" in names
        assert "formulario_enel_ce.pdf" in names
        for name in names:
            assert len(zf.read(name)) > 0, f"{name} should not be empty"


def test_generate_memorial_v2(client, token, inversor, placa):
    """POST /docs/v2/memorialdescritivo fetches equipment specs from DB by ID."""
    payload = {
        **MEMORIAL_V2_BASE,
        "inversores": [{"id_inversor": inversor.id_inversor, "quantidade": 1}],
        "placas": [{"id_placa": placa.id_placa, "quantidade": 10}],
    }
    response = client.post(
        "/docs/v2/memorialdescritivo",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    _assert_pdf_response(response)


def test_generate_diagrama_unifilar_v2(client, token, inversor, placa):
    """POST /docs/v2/diagramaunifilar fetches equipment specs from DB by ID."""
    payload = {
        **UNIFILAR_V2_BASE,
        "sistemas": [
            {
                "id_inversor": inversor.id_inversor,
                "quantidade_inversor": 1,
                "id_placa": placa.id_placa,
                "quantidade_placas": 10,
            }
        ],
    }
    response = client.post(
        "/docs/v2/diagramaunifilar",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    _assert_pdf_response(response)


def test_generate_diagrama_unifilar_v2_dois_sistemas(client, token, inversor, placa):
    """Two-system diagram returns a valid PDF."""
    payload = {
        **UNIFILAR_V2_BASE,
        "sistemas": [
            {"id_inversor": inversor.id_inversor, "quantidade_inversor": 1,
             "id_placa": placa.id_placa, "quantidade_placas": 10},
            {"id_inversor": inversor.id_inversor, "quantidade_inversor": 1,
             "id_placa": placa.id_placa, "quantidade_placas": 8},
        ],
    }
    response = client.post(
        "/docs/v2/diagramaunifilar",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    _assert_pdf_response(response)


def test_generate_diagrama_unifilar_v2_inversor_not_found(client, token, placa):
    payload = {
        **UNIFILAR_V2_BASE,
        "sistemas": [
            {"id_inversor": 99999, "quantidade_inversor": 1,
             "id_placa": placa.id_placa, "quantidade_placas": 10},
        ],
    }
    response = client.post(
        "/docs/v2/diagramaunifilar",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_generate_diagrama_unifilar_v2_placa_not_found(client, token, inversor):
    payload = {
        **UNIFILAR_V2_BASE,
        "sistemas": [
            {"id_inversor": inversor.id_inversor, "quantidade_inversor": 1,
             "id_placa": 99999, "quantidade_placas": 10},
        ],
    }
    response = client.post(
        "/docs/v2/diagramaunifilar",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_generate_memorial_v2_inversor_not_found(client, token, placa):
    """POST /docs/v2/memorialdescritivo returns 404 for unknown inversor ID."""
    payload = {
        **MEMORIAL_V2_BASE,
        "inversores": [{"id_inversor": 99999, "quantidade": 1}],
        "placas": [{"id_placa": placa.id_placa, "quantidade": 10}],
    }
    response = client.post(
        "/docs/v2/memorialdescritivo",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_generate_memorial_v2_placa_not_found(client, token, inversor):
    """POST /docs/v2/memorialdescritivo returns 404 for unknown placa ID."""
    payload = {
        **MEMORIAL_V2_BASE,
        "inversores": [{"id_inversor": inversor.id_inversor, "quantidade": 1}],
        "placas": [{"id_placa": 99999, "quantidade": 10}],
    }
    response = client.post(
        "/docs/v2/memorialdescritivo",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_todos_endpoint_requires_auth(client):
    """POST /docs/todos should return 401 when no token is provided."""
    response = client.post("/docs/todos", json=COMPLETO_PAYLOAD)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_docs_endpoint_requires_auth(client):
    """Endpoints should return 401 when no token is provided."""
    response = client.post(
        "/docs/memorialdescritivo",
        json=MEMORIAL_PAYLOAD,
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


