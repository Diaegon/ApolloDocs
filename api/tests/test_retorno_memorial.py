"""
Regression test for ObjetosCalculados.construtor_dados_memorial().

Purpose: Snapshot the *structure* of RetornoProjetoCompleto so that
refactoring creatememorialobject.py doesn't silently break the DTO
shape the PDF builder depends on.

Assertions:
- All expected fields are present on the returned DTO.
- Key derived values (energia_gerada_mensal, potencia_efetiva, etc.)
  are numeric and non-zero given a realistic payload.
- Text lists (texto_cabos, texto_2_protecao_inversor) are populated.
"""

from dataclasses import fields

import pytest

from api.schemas.projetos.memorial import ProjetoMemorial
from api.tests.test_payloads import MEMORIAL_PAYLOAD, MEMORIAL_PAYLOAD1_2
from src.createproject import ProjectFactory
from src.domain.creatememorialobject import ObjetosCalculados
from src.schemas.modelreturnobject import RetornoProjetoCompleto

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def retorno() -> RetornoProjetoCompleto:
    """Build RetornoProjetoCompleto from the standard test payload."""
    dados = ProjetoMemorial(**MEMORIAL_PAYLOAD)
    projeto = ProjectFactory.factory(dados)
    obj = ObjetosCalculados(projeto).calculate()
    return obj.construtor_dados_memorial()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

# All declared fields in the RetornoProjetoCompleto dataclass
EXPECTED_FIELDS = {f.name for f in fields(RetornoProjetoCompleto)}


def test_retorno_has_all_expected_fields(retorno):
    """Every field declared in RetornoProjetoCompleto must be present."""
    actual_fields = {f.name for f in fields(retorno)}
    assert actual_fields == EXPECTED_FIELDS, (
        f"Fields mismatch.\n"
        f"Missing: {EXPECTED_FIELDS - actual_fields}\n"
        f"Extra  : {actual_fields - EXPECTED_FIELDS}"
    )


def test_potencia_efetiva_is_nonzero(retorno):
    """potencia_efetiva must be a positive number for a real system."""
    assert isinstance(retorno.potencia_efetiva, (int, float))
    assert retorno.potencia_efetiva > 0


def test_energia_gerada_mensal_is_nonzero(retorno):
    """energia_gerada_mensal must be a positive number."""
    assert isinstance(retorno.energia_gerada_mensal, (int, float))
    assert retorno.energia_gerada_mensal > 0


def test_texto_inversores_is_populated(retorno):
    """texto_inversor_memorial must contain the inverter brand/model."""
    assert "Fronius" in retorno.texto_inversor_memorial
    assert "Symo 5.0" in retorno.texto_inversor_memorial


def test_texto_placas_is_populated(retorno):
    """texto_placas_memorial must contain the panel brand/model."""
    assert "Canadian Solar" in retorno.texto_placas_memorial
    assert "CS6R-500MS" in retorno.texto_placas_memorial


def test_texto_cabos_is_a_list(retorno):
    """texto_cabos should be a list of cable strings, one per system."""
    assert isinstance(retorno.texto_cabos, list)
    assert len(retorno.texto_cabos) >= 1
    for cabo in retorno.texto_cabos:
        assert isinstance(cabo, str)
        assert "mm²" in cabo


def test_disjuntor_protecao_is_a_list(retorno):
    """texto_2_protecao_inversor should be a list of ints."""
    assert isinstance(retorno.texto_2_protecao_inversor, list)
    assert len(retorno.texto_2_protecao_inversor) >= 1
    for dj in retorno.texto_2_protecao_inversor:
        assert isinstance(dj, int)


def test_cidade_obra_is_correct(retorno):
    """Address fields should be correctly mapped."""
    assert retorno.cidade_obra == "Fortaleza"
    assert retorno.estado_obra == "CE"


def test_nome_cliente_is_correct(retorno):
    """Client fields should be correctly mapped."""
    assert retorno.nome_cliente == "João da Silva"


def test_numero_uc_is_correct(retorno):
    """numero_uc should be mapped from the input."""
    assert retorno.numero_uc == "1234567890"


def test_equacoes_are_strings(retorno):
    """All 4 equations should be non-empty strings."""
    for eq_name in ("equacao", "equacao2", "equacao4"):
        value = getattr(retorno, eq_name)
        assert isinstance(value, str) and len(value) > 0, (
            f"{eq_name} should be a non-empty string"
        )
    # equacao3 is a list of equations (one per system)
    assert isinstance(retorno.equacao3, list)
    assert len(retorno.equacao3) >= 1
