from pydantic import BaseModel

from api.schemas.cliente.cliente import Cliente
from api.schemas.cliente.endereco import EnderecoObra
from api.schemas.common.enums import (
    classe_consumo,
    ramal_de_energia,
    tensao_fase,
)
from api.schemas.sistema.materiais import MaterialInversorRef, MaterialPlacaRef


class ProjetoMemorialV2(BaseModel):
    model_config = {"use_enum_values": True}
    id_projeto: int | None = None

    cliente: Cliente | None = None
    endereco_obra: EnderecoObra | None = None

    numero_unidade_consumidora: str
    carga_instalada_kw: float = 10.0
    disjuntor_geral_amperes: float = 40.0
    energia_media_mensal_kwh: float = 200.0
    classe_consumo1: (
        classe_consumo  # residencial, comercial, industrial, rural
    )
    tipo_fornecimento: tensao_fase  # monofasico, bifasico, trifasico
    ramal_energia: ramal_de_energia  # aéreo, subterrâneo
    data_projeto: str

    inversores: list[MaterialInversorRef]
    placas: list[MaterialPlacaRef]
