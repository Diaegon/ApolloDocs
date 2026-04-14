from pydantic import BaseModel, field_validator, model_validator

from api.schemas.cliente.cliente import ClienteSchema
from api.schemas.cliente.endereco import EnderecoClienteSchema, EnderecoObraSchema
from api.schemas.common.enums import (
    classe_consumo,
    ramal_de_energia,
    tensao_fase,
)
from api.schemas.pessoas.procurador import ProcuradorSchema
from api.schemas.sistema.materiais import MaterialInversorRef, MaterialPlacaRef


class ProjetoTodos(BaseModel):
    """
    Unified schema for generating all documents in a single request.

    The service maps it to each individual document generator and returns
    a ZIP with all 4 PDFs.

    Field-to-document mapping
    ─────────────────────────
    nome_projetista / cft_crea_projetista → unifilar
    cliente                → memorial, procuracao; nome/cpf/tel/email → unifilar, formulario
    endereco_cliente        → procuracao
    endereco_obra           → all four
    procurador              → procuracao; nome/cpf/email/tel → formulario
    numero_unidade_consumidora → memorial, formulario
    carga_instalada_kw      → memorial, formulario
    disjuntor_geral_amperes → memorial, unifilar
    energia_media_mensal_kwh → memorial
    classe_consumo          → memorial, formulario
    tipo_fornecimento       → memorial
    ramal_energia           → memorial, formulario
    tensao_local            → unifilar, formulario
    potencia_geracao        → formulario
    data_projeto            → memorial, formulario
    inversores / placas     → memorial, unifilar (fetched from DB by ID)
    """

    model_config = {"use_enum_values": True}

    # ── Projetista ──────────────────────────────────────────────────────────
    nome_projetista: str = "[NOME DO PROJETISTA]"
    cft_crea_projetista: str = "[CFT ou CREA DO PROJETISTA]"

    # ── Partes ──────────────────────────────────────────────────────────────
    cliente: ClienteSchema
    endereco_cliente: EnderecoClienteSchema
    endereco_obra: EnderecoObraSchema
    procurador: ProcuradorSchema

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

    # ── Equipamentos (ID refs — specs fetched from DB) ──────────────────────
    inversores: list[MaterialInversorRef]
    placas: list[MaterialPlacaRef]

    @field_validator("inversores", "placas")
    @classmethod
    def validate_length(cls, v):
        if not 1 <= len(v) <= 3:
            raise ValueError("must have between 1 and 3 entries")
        return v

    @model_validator(mode="after")
    def validate_matching_lengths(self):
        if len(self.inversores) != len(self.placas):
            raise ValueError("inversores and placas must have the same length")
        return self
