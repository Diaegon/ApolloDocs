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
    PROCURACAO_PAYLOAD,
    UNIFILAR_PAYLOAD,
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


