from pydantic import BaseModel, field_validator, model_validator

from api.schemas.cliente.endereco import EnderecoObra
from api.schemas.sistema.materiais import MaterialInversorRef, MaterialPlacaRef


class ProjetoUnifilarV2(BaseModel):
    nome_projetista: str = "[NOME DO PROJETISTA]"
    cft_crea_projetista: str = "[CFT ou CREA DO PROJETISTA]"
    nome_cliente: str
    disjuntor_geral_amperes: float = 40.0
    tensao_local: int
    endereco_obra: EnderecoObra
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
