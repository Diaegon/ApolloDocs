from pydantic import BaseModel, ConfigDict


class PlacaSchema(BaseModel):
    marca_placa: str
    modelo_placa: str
    potencia_placa: float
    tipo_celula: str
    tensao_pico: float
    corrente_curtocircuito: float
    tensao_maxima_potencia: float
    corrente_maxima_potencia: float
    eficiencia_placa: float | None = None


class PlacaPublic(PlacaSchema):
    id_placa: int
    model_config = ConfigDict(from_attributes=True)


class PlacaList(BaseModel):
    placas: list[PlacaPublic]
