"""
Tests for document generation endpoints in /docs.

Strategy:
- Each test authenticates as a valid user, submits a standard payload,
  and asserts the response is a downloadable PDF file.
- No assertions are made about document content, only about delivery.
"""

from http import HTTPStatus

# ---------------------------------------------------------------------------
# Shared payload fixtures
# ---------------------------------------------------------------------------

SISTEMA_INSTALADO_1 = {
    "inversor": {
        "id_inversor": None,
        "marca_inversor": "Fronius",
        "modelo_inversor": "Symo 5.0",
        "potencia_inversor": 5.0,   # in kW as used by the calculation engine
        "numero_fases": "monofasico",
        "tipo_de_inversor": "string",
        "numero_mppt": 2,
    },
    "quantidade_inversor": 1,
    "quantidade_total_placas_do_sistema": {
        "quantidade_placas": 10,
        "quantidade_placas2": None,
    },
    "placa": {
        "id_placa": None,
        "marca_placa": "Canadian Solar",
        "modelo_placa": "CS6R-500MS",
        "potencia_placa": 500.0,
        "tipo_celula": "Monocristalino",
        "tensao_pico": 49.3,
        "corrente_curtocircuito": 13.58,
        "tensao_maxima_potencia": 41.8,
        "corrente_maxima_potencia": 11.97,
        "eficiencia_placa": None,
    },
    "placa2": None,
}

ENDERECO_OBRA = {
    "logradouro_obra": "Rua das Flores",
    "numero_obra": "100",
    "complemento_obra": "",   # empty string so it's not excluded by exclude_none
    "cep_obra": "60000-000",
    "bairro_obra": "Centro",
    "cidade_obra": "Fortaleza",
    "estado_obra": "CE",
    "latitude_obra": "-3.7172",
    "longitude_obra": "-38.5431",
}

CLIENTE = {
    "id_cliente": 1,
    "nome_cliente": "João da Silva",
    "cpf": "000.000.000-00",
    "data_nascimento": "01/01/1990",
    "razao_social": "",          # PF client — empty but present
    "nome_fantasia": "",
    "cnpj": "",
    "rg": "0000000",
    "telefone_cliente": "85 999999999",
    "email_cliente": "joao@email.com",
}

PROCURADOR = {
    "id_procurador": None,
    "nome_procurador": "Maria Engenheira",
    "cpf_procurador": "111.111.111-11",
    "rg_procurador": "1111111",
    "telefone_procurador": "85 988888888",
    "email_procurador": "maria@eng.br",
    "logradouro_procurador": "Av. Principal",
    "numero_casa_procurador": "200",
    "complemento_procurador": None,
    "cep_procurador": "60000-001",
    "bairro_procurador": "Meireles",
    "cidade_procurador": "Fortaleza",
    "estado_procurador": "CE",
}

MEMORIAL_PAYLOAD = {
    "id_projeto": 1,
    "cliente": CLIENTE,
    "endereco_obra": ENDERECO_OBRA,
    "numero_unidade_consumidora": "1234567890",
    "carga_instalada_kw": 10.0,
    "disjuntor_geral_amperes": 40.0,
    "energia_media_mensal_kwh": 400.0,
    "classe_consumo1": "residencial",
    "tipo_fornecimento": "monofasico",
    "ramal_energia": "aereo",
    "data_projeto": "2026-03-05",
    "quantidade_sistemas_instalados": 1,
    "sistema_instalado1": SISTEMA_INSTALADO_1,
    "sistema_instalado2": None,
    "sistema_instalado3": None,
}

PROCURACAO_PAYLOAD = {
    "id_projeto": 1,
    "cliente": CLIENTE,
    "endereco_cliente": {
        "logradouro_cliente": "Rua das Flores",
        "numero_casa_cliente": "100",
        "complemento_casa_cliente": None,
        "cep_cliente": "60000-000",
        "bairro_cliente": "Centro",
        "cidade_cliente": "Fortaleza",
        "estado_cliente": "CE",
    },
    "endereco_obra": ENDERECO_OBRA,
    "procurador": PROCURADOR,
}

UNIFILAR_PAYLOAD = {
    "nome_projetista": "Maria Engenheira",
    "cft_crea_projetista": "CREA-CE 123456",
    "nome_cliente": "João da Silva",
    "quantidade_sistemas_instalados": 1,
    "disjuntor_geral_amperes": 40.0,
    "tensao_local": 220,
    "endereco_obra": ENDERECO_OBRA,
    "sistema_instalado1": SISTEMA_INSTALADO_1,
    "sistema_instalado2": None,
    "sistema_instalado3": None,
}

FORMULARIO_PAYLOAD = {
    "numero_uc": "1234567890",
    "classe": "residencial",
    "ramal_energia": "aereo",
    "nome_cliente": "João da Silva",
    "cpf": "000.000.000-00",
    "telefone_cliente": "85 999999999",
    "email_cliente": "joao@email.com",
    "endereco_obra": ENDERECO_OBRA,
    "tensao_local": 220,
    "carga_instalada_kw": 8.0,
    "potencia_geracao": 5,
    "nome_procurador": "Maria Engenheira",
    "cpf_procurador": "111.111.111-11",
    "email_procurador": "maria@eng.br",
    "data_hoje": "05/03/2026",
    "telefone_procurador": "85 988888888",
}


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
