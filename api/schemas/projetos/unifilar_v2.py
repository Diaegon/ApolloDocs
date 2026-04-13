from pydantic import BaseModel, field_validator

from api.schemas.cliente.endereco import EnderecoObra


class SistemaUnifilarRef(BaseModel):
    id_inversor: int
    quantidade_inversor: int = 1
    id_placa: int
    quantidade_placas: int = 10


class ProjetoUnifilarV2(BaseModel):
    nome_projetista: str = "[NOME DO PROJETISTA]"
    cft_crea_projetista: str = "[CFT ou CREA DO PROJETISTA]"
    nome_cliente: str
    disjuntor_geral_amperes: float = 40.0
    tensao_local: int
    endereco_obra: EnderecoObra
    sistemas: list[SistemaUnifilarRef]

    @field_validator("sistemas")
    @classmethod
    def validate_sistemas(cls, v):
        if not 1 <= len(v) <= 3:
            raise ValueError("sistemas must have between 1 and 3 entries")
        return v
