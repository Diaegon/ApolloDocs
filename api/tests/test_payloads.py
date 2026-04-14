"""
Shared payloads and data for API tests.
"""

ENDERECO_OBRA = {
    "logradouro_obra": "Rua das Flores",
    "numero_obra": "100",
    "complemento_obra": "",
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
    "razao_social": "",
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

# ── V2 base payloads (equipment IDs added by tests using fixtures) ──────────

UNIFILAR_V2_BASE = {
    "nome_projetista": "Maria Engenheira",
    "cft_crea_projetista": "CREA-CE 123456",
    "nome_cliente": "João da Silva",
    "disjuntor_geral_amperes": 40.0,
    "tensao_local": 220,
    "endereco_obra": ENDERECO_OBRA,
}

MEMORIAL_V2_BASE = {
    "cliente": CLIENTE,
    "endereco_obra": ENDERECO_OBRA,
    "numero_unidade_consumidora": "1234567890",
    "carga_instalada_kw": 10.0,
    "disjuntor_geral_amperes": 40.0,
    "energia_media_mensal_kwh": 400.0,
    "classe_consumo1": "residencial",
    "tipo_fornecimento": "monofasico",
    "ramal_energia": "aereo",
    "data_projeto": "2026-03-06",
}

COMPLETO_V2_BASE = {
    "nome_projetista": "Maria Engenheira",
    "cft_crea_projetista": "CREA-CE 123456",
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
    "numero_unidade_consumidora": "1234567890",
    "carga_instalada_kw": 10.0,
    "disjuntor_geral_amperes": 40.0,
    "energia_media_mensal_kwh": 400.0,
    "classe_consumo": "residencial",
    "tipo_fornecimento": "monofasico",
    "ramal_energia": "aereo",
    "tensao_local": 220,
    "potencia_geracao": 5,
    "data_projeto": "2026-03-06",
}
