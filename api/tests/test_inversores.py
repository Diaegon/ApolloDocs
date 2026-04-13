from http import HTTPStatus
import pytest
from unittest.mock import patch

@patch("api.routers.inversores.os.path.exists")
@patch("api.routers.inversores.os.listdir")
@patch("api.routers.inversores.os.path.isdir")
@patch("api.routers.inversores.os.path.isfile")
def test_list_inversores(mock_isfile, mock_isdir, mock_listdir, mock_exists, client, token):
    """GET /inversores/list should return a tree of brands and models."""
    mock_exists.return_value = True

    def side_effect_listdir(path):
        if "INMETRO_INVERSORES" in path and "BRAND_A" not in path:
            return ["BRAND_A"]
        elif "BRAND_A" in path and "MODEL_1" not in path:
            return ["MODEL_1"]
        elif "MODEL_1" in path:
            return ["document.pdf", "image.png"]
        return []

    mock_listdir.side_effect = side_effect_listdir
    mock_isdir.return_value = True
    # Only recognize .pdf as file for this test mock
    mock_isfile.side_effect = lambda p: p.endswith(".pdf") or p.endswith(".png")

    response = client.get(
        "/inversores/list",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["brand"] == "BRAND_A"
    assert len(data[0]["models"]) == 1
    assert data[0]["models"][0]["name"] == "MODEL_1"
    assert data[0]["models"][0]["files"] == ["document.pdf"] # Expect only .pdf files

def test_list_inversores_unauthorized(client):
    """GET /inversores/list should return 401 when no token is provided."""
    response = client.get("/inversores/list")
    assert response.status_code == HTTPStatus.UNAUTHORIZED

def test_inversor_v2_schema():
    """Test that Inversor_v2 schema correctly stores brand, model and quantity."""
    from api.schemas.sistema.inversor import Inversor_v2
    inversor = Inversor_v2(marca_inversor="Fronius", modelo_inversor="Symo 5.0", quantidade=2)
    assert inversor.marca_inversor == "Fronius"
    assert inversor.modelo_inversor == "Symo 5.0"
    assert inversor.quantidade == 2
