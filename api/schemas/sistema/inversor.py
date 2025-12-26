from pydantic import BaseModel

from api.schemas.common.enums import tensao_fase, tipo_inversor


class Inversor(BaseModel):
    id_inversor: int | None
    marca_inversor: str = "[MARCA DO INVERSOR]"
    modelo_inversor: str = "[MODELO DO INVERSOR]"
    potencia_inversor: float = 0.0
    numero_fases: tensao_fase = "monofasico"
    tipo_de_inversor: tipo_inversor = "string"
    numero_mppt: int | None = 4  # reservado para atualizações futuras
