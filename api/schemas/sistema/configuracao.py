from pydantic import BaseModel

from api.schemas.sistema.inversor import Inversor
from api.schemas.sistema.placas import Placa


class QuantidadePlacas(BaseModel):
    quantidade_placas: int = 10
    quantidade_placas2: int | None = None


class ConfiguracaoSistema(BaseModel):
    inversor: Inversor
    quantidade_inversor: int = 1
    quantidade_total_placas_do_sistema: QuantidadePlacas
    placa: Placa
    placa2: Placa | None = None
