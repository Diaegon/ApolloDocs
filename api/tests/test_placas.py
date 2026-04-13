from api.schemas.sistema.placas import Placa_v2

def test_placa_v2_schema():
    """Test that Placa_v2 schema correctly stores brand, model and quantity."""
    placa = Placa_v2(marca_placa="Canadian Solar", modelo_placa="CS6W-550MS", quantidade=10)
    assert placa.marca_placa == "Canadian Solar"
    assert placa.modelo_placa == "CS6W-550MS"
    assert placa.quantidade == 10
