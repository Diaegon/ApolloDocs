"""
Shared payloads and data for API tests.
Commonly used in test_docs.py and test_retorno_memorial.py.
"""

SISTEMA_INSTALADO_1 = {
    "inversor": {
        "id_inversor": None,
        "marca_inversor": "Fronius",
        "modelo_inversor": "Symo 5.0",
        "potencia_inversor": 5.0,
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

SISTEMA_INSTALADO1_2 = {
    "inversor": {
        "id_inversor": None,
        "marca_inversor": "Fronius",
        "modelo_inversor": "Symo 5.0",
        "potencia_inversor": 5.0,
        "numero_fases": "monofasico",
        "tipo_de_inversor": "string",
        "numero_mppt": 2,
    },
    "quantidade_inversor": 1,
    "quantidade_total_placas_do_sistema": {
        "quantidade_placas": 10,
        "quantidade_placas2": 10,
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
    "placa2": {
        "id_placa": None,
        "marca_placa": "TRINA",
        "modelo_placa": "TSM-DE09.08-440",
        "potencia_placa": 440.0,
        "tipo_celula": "Monocristalino",
        "tensao_pico": 49.3,
        "corrente_curtocircuito": 13.58,
        "tensao_maxima_potencia": 41.8,
        "corrente_maxima_potencia": 11.97,
        "eficiencia_placa": None,
    },
}

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
    "data_projeto": "2026-03-06",
    "quantidade_sistemas_instalados": 1,
    "sistema_instalado1": SISTEMA_INSTALADO_1,
    "sistema_instalado2": None,
    "sistema_instalado3": None,
}

MEMORIAL_PAYLOAD1_2 = {
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
    "data_projeto": "2026-03-06",
    "quantidade_sistemas_instalados": 1,
    "sistema_instalado1": SISTEMA_INSTALADO1_2,
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

COMPLETO_PAYLOAD = {
    "id_projeto": 1,
    # Projetista
    "nome_projetista": "Maria Engenheira",
    "cft_crea_projetista": "CREA-CE 123456",
    # Partes
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
    # Dados do projeto
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
    # Sistemas
    "quantidade_sistemas_instalados": 1,
    "sistema_instalado1": SISTEMA_INSTALADO_1,
    "sistema_instalado2": None,
    "sistema_instalado3": None,
}

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
