from pydantic import BaseModel

from api.schemas.cliente.cliente import Cliente
from api.schemas.cliente.endereco import EnderecoCliente, EnderecoObra
from api.schemas.common.enums import (
    classe_consumo,
    ramal_de_energia,
    tensao_fase,
)
from api.schemas.pessoas.procurador import Procurador
from api.schemas.sistema.configuracao import ConfiguracaoSistema


class ProjetoTodos(BaseModel):
    """
    Unified schema for generating all documents in a single request.

    The user fills data once; the AllDocsService maps it to each individual
    schema (ProjetoMemorial, ProjetoProcuracao, ProjetoUnifilar,
    ProjetoFormularioEnelCe) and returns a ZIP with all 4 PDFs.

    Field-to-document mapping
    ─────────────────────────
    id_projeto              → memorial, procuracao
    nome_projetista         → unifilar
    cft_crea_projetista     → unifilar
    cliente                 → memorial, procuracao; nome/cpf/tel/email → unifilar, formulario
    endereco_cliente        → procuracao
    endereco_obra           → all four
    procurador              → procuracao; nome/cpf/email/tel → formulario
    numero_unidade_consumidora → memorial (campo), formulario (numero_uc)
    carga_instalada_kw      → memorial, formulario
    disjuntor_geral_amperes → memorial, unifilar
    energia_media_mensal_kwh → memorial
    classe_consumo          → memorial (classe_consumo1), formulario (classe)
    tipo_fornecimento       → memorial
    ramal_energia           → memorial, formulario
    tensao_local            → unifilar, formulario
    potencia_geracao        → formulario
    data_projeto            → memorial (data_projeto), formulario (data_hoje)
    quantidade_sistemas_instalados → memorial, unifilar
    sistema_instalado1/2/3  → memorial, unifilar
    """

    model_config = {"use_enum_values": True}

    id_projeto: int | None

    # ── Projetista ──────────────────────────────────────────────────────────
    nome_projetista: str = "[NOME DO PROJETISTA]"
    cft_crea_projetista: str = "[CFT ou CREA DO PROJETISTA]"

    # ── Partes ──────────────────────────────────────────────────────────────
    cliente: Cliente
    endereco_cliente: EnderecoCliente
    endereco_obra: EnderecoObra
    procurador: Procurador

    # ── Dados do projeto ────────────────────────────────────────────────────
    numero_unidade_consumidora: str
    carga_instalada_kw: float = 10.0
    disjuntor_geral_amperes: float = 40.0
    energia_media_mensal_kwh: float = 200.0
    classe_consumo: classe_consumo
    tipo_fornecimento: tensao_fase
    ramal_energia: ramal_de_energia
    tensao_local: int = 220
    potencia_geracao: int = 8
    data_projeto: str

    # ── Sistemas fotovoltaicos ──────────────────────────────────────────────
    quantidade_sistemas_instalados: int = 1
    sistema_instalado1: ConfiguracaoSistema
    sistema_instalado2: ConfiguracaoSistema | None = None
    sistema_instalado3: ConfiguracaoSistema | None = None
