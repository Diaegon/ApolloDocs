"""
Domain unit tests for ObjetoDiagramaUnifilarV2.

Tests only the domain layer — no HTTP, no DB.
The service layer integration is covered in test_docs.py.
"""

import pytest
from api.schemas.sistema.inversor import Inversor
from api.schemas.sistema.placas import Placa
from src.domain.creatediagramobject_v2 import (
    ObjetoDiagramaUnifilarV2,
    ProjetoUnifilarResolvido,
    SistemaResolvidoV2,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _make_inversor(potencia=5000.0, fases="monofasico", mppt=2):
    return Inversor(
        id_inversor=1,
        marca_inversor="DEYE",
        modelo_inversor="SUN-5K",
        potencia_inversor=potencia,
        numero_fases=fases,
        tipo_de_inversor="string",
        numero_mppt=mppt,
    )


def _make_placa(potencia=410.0):
    return Placa(
        id_placa=1,
        marca_placa="CANADIAN SOLAR",
        modelo_placa="CS6R-410H",
        potencia_placa=potencia,
        tipo_celula="monocrystalino",
        tensao_pico=49.3,
        corrente_curtocircuito=11.09,
        tensao_maxima_potencia=41.8,
        corrente_maxima_potencia=9.82,
        eficiencia_placa=21.4,
    )


def _make_projeto(sistemas, tensao_local=220):
    return ProjetoUnifilarResolvido(
        nome_projetista="Maria Eng.",
        cft_crea_projetista="CREA-CE 123",
        nome_cliente="João Silva",
        disjuntor_geral_amperes=40.0,
        tensao_local=tensao_local,
        endereco_obra=None,
        sistemas=sistemas,
    )


# ── Quantidade de sistemas ────────────────────────────────────────────────────

def test_um_sistema():
    projeto = _make_projeto([
        SistemaResolvidoV2(
            inversor=_make_inversor(), quantidade_inversor=1,
            placa=_make_placa(), quantidade_placas=10,
        )
    ])
    retorno = ObjetoDiagramaUnifilarV2(projeto).construir_dados_diagrama()
    assert retorno.quantidade_sistemas_instalados == 1
    assert retorno.sistema_instalado2 is None
    assert retorno.sistema_instalado3 is None


def test_dois_sistemas():
    projeto = _make_projeto([
        SistemaResolvidoV2(_make_inversor(), 1, _make_placa(), 10),
        SistemaResolvidoV2(_make_inversor(), 1, _make_placa(), 8),
    ])
    retorno = ObjetoDiagramaUnifilarV2(projeto).construir_dados_diagrama()
    assert retorno.quantidade_sistemas_instalados == 2
    assert retorno.sistema_instalado2 is not None
    assert retorno.sistema_instalado3 is None


def test_tres_sistemas():
    projeto = _make_projeto([
        SistemaResolvidoV2(_make_inversor(), 1, _make_placa(), 10),
        SistemaResolvidoV2(_make_inversor(), 1, _make_placa(), 8),
        SistemaResolvidoV2(_make_inversor(), 1, _make_placa(), 6),
    ])
    retorno = ObjetoDiagramaUnifilarV2(projeto).construir_dados_diagrama()
    assert retorno.quantidade_sistemas_instalados == 3
    assert retorno.sistema_instalado3 is not None


# ── Cálculos de potência ──────────────────────────────────────────────────────

def test_potencia_total_inversores_em_watts():
    """potencia_total_inversores deve acumular em W (5000 * 2 = 10000)."""
    projeto = _make_projeto([
        SistemaResolvidoV2(_make_inversor(5000.0), 2, _make_placa(), 10),
    ])
    retorno = ObjetoDiagramaUnifilarV2(projeto).construir_dados_diagrama()
    assert retorno.potencia_total_inversores == 10000.0


def test_potencia_total_placas_em_watts():
    """potencia_total_placas deve acumular em Wp (410 * 10 = 4100)."""
    projeto = _make_projeto([
        SistemaResolvidoV2(_make_inversor(), 1, _make_placa(410.0), 10),
    ])
    retorno = ObjetoDiagramaUnifilarV2(projeto).construir_dados_diagrama()
    assert retorno.potencia_total_placas == 4100.0


def test_potencia_total_acumula_multiplos_sistemas():
    projeto = _make_projeto([
        SistemaResolvidoV2(_make_inversor(5000.0), 1, _make_placa(410.0), 10),
        SistemaResolvidoV2(_make_inversor(6000.0), 1, _make_placa(500.0), 8),
    ])
    retorno = ObjetoDiagramaUnifilarV2(projeto).construir_dados_diagrama()
    assert retorno.potencia_total_inversores == 11000.0
    assert retorno.potencia_total_placas == 410.0 * 10 + 500.0 * 8


# ── Textos gerados ────────────────────────────────────────────────────────────

def test_texto_inversor_formato():
    projeto = _make_projeto([
        SistemaResolvidoV2(_make_inversor(5000.0), 1, _make_placa(), 10),
    ])
    retorno = ObjetoDiagramaUnifilarV2(projeto).construir_dados_diagrama()
    assert "DEYE" in retorno.texto_inversor1
    assert "SUN-5K" in retorno.texto_inversor1
    assert "5.0 kW" in retorno.texto_inversor1


def test_texto_paineis_formato():
    projeto = _make_projeto([
        SistemaResolvidoV2(_make_inversor(), 1, _make_placa(), 12),
    ])
    retorno = ObjetoDiagramaUnifilarV2(projeto).construir_dados_diagrama()
    assert "12x" in retorno.texto_paineis1
    assert "CANADIAN SOLAR" in retorno.texto_paineis1


def test_texto_disjuntor_geral_monofasico():
    projeto = _make_projeto(
        [SistemaResolvidoV2(_make_inversor(), 1, _make_placa(), 10)],
        tensao_local=220,
    )
    retorno = ObjetoDiagramaUnifilarV2(projeto).construir_dados_diagrama()
    assert "MONOFÁSICO" in retorno.texto_disjuntorgeral_unifilar
    assert "220V" in retorno.texto_disjuntorgeral_unifilar


def test_texto_disjuntor_geral_trifasico():
    projeto = _make_projeto(
        [SistemaResolvidoV2(_make_inversor(fases="trifasico"), 1, _make_placa(), 10)],
        tensao_local=380,
    )
    retorno = ObjetoDiagramaUnifilarV2(projeto).construir_dados_diagrama()
    assert "TRIFÁSICO" in retorno.texto_disjuntorgeral_unifilar


def test_texto_disjuntor_protecao_monofasico():
    # 5000W monofasico: 5000 / 220 = 22.7A → disjuntor 25A
    projeto = _make_projeto([
        SistemaResolvidoV2(_make_inversor(5000.0, "monofasico"), 1, _make_placa(), 10),
    ])
    retorno = ObjetoDiagramaUnifilarV2(projeto).construir_dados_diagrama()
    assert "25 A" in retorno.texto_disjuntor_protecao1
    assert "MONOFÁSICO" in retorno.texto_disjuntor_protecao1


# ── ConfiguracaoSistema gerada (usada pelo PDF builder) ───────────────────────

def test_sistema_instalado1_tem_inversor_correto():
    inv = _make_inversor(5000.0, "monofasico")
    projeto = _make_projeto([
        SistemaResolvidoV2(inv, 1, _make_placa(), 10),
    ])
    retorno = ObjetoDiagramaUnifilarV2(projeto).construir_dados_diagrama()
    assert retorno.sistema_instalado1 is not None
    assert retorno.sistema_instalado1.inversor.numero_fases == "monofasico"
    assert retorno.sistema_instalado1.inversor.marca_inversor == "DEYE"


def test_sistema_instalado1_tem_quantidade_placas_correta():
    projeto = _make_projeto([
        SistemaResolvidoV2(_make_inversor(), 1, _make_placa(), 15),
    ])
    retorno = ObjetoDiagramaUnifilarV2(projeto).construir_dados_diagrama()
    assert retorno.sistema_instalado1.quantidade_total_placas_do_sistema.quantidade_placas == 15
