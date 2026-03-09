"""
Tests for document generation endpoints in /docs.

Strategy:
- Each test authenticates as a valid user, submits a standard payload,
  and asserts the response is a downloadable PDF file.
- No assertions are made about document content, only about delivery.
"""

from http import HTTPStatus
from api.tests.test_payloads import MEMORIAL_PAYLOAD, PROCURACAO_PAYLOAD, UNIFILAR_PAYLOAD, FORMULARIO_PAYLOAD


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
        f"/docs/memorialdescritivo?user_id={user.id}",
        json=MEMORIAL_PAYLOAD,
        headers={"Authorization": f"Bearer {token}"},
    )
    _assert_pdf_response(response)


def test_generate_procuracao(client, user, token):
    """POST /docs/procuracao should return a downloadable PDF."""
    response = client.post(
        f"/docs/procuracao?user_id={user.id}",
        json=PROCURACAO_PAYLOAD,
        headers={"Authorization": f"Bearer {token}"},
    )
    _assert_pdf_response(response)


def test_generate_diagrama_unifilar(client, user, token):
    """POST /docs/diagramaunifilar should return a downloadable PDF."""
    response = client.post(
        f"/docs/diagramaunifilar?user_id={user.id}",
        json=UNIFILAR_PAYLOAD,
        headers={"Authorization": f"Bearer {token}"},
    )
    _assert_pdf_response(response)


def test_generate_formulario_enel(client, user, token):
    """POST /docs/formularioenel should return a downloadable PDF."""
    response = client.post(
        f"/docs/formularioenel?user_id={user.id}",
        json=FORMULARIO_PAYLOAD,
        headers={"Authorization": f"Bearer {token}"},
    )
    _assert_pdf_response(response)


def test_docs_endpoint_requires_auth(client):
    """Endpoints should return 401 when no token is provided."""
    response = client.post(
        "/docs/memorialdescritivo?user_id=1",
        json=MEMORIAL_PAYLOAD,
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_docs_endpoint_rejects_wrong_user(client, user, token):
    """Endpoints should return 403 when user_id doesn't match the token."""
    wrong_user_id = user.id + 99
    response = client.post(
        f"/docs/memorialdescritivo?user_id={wrong_user_id}",
        json=MEMORIAL_PAYLOAD,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
