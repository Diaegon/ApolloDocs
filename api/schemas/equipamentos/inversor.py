from pydantic import BaseModel, ConfigDict

from api.schemas.common.enums import tensao_fase, tipo_inversor


class InversorSchema(BaseModel):
    marca_inversor: str
    modelo_inversor: str
    potencia_inversor: float
    numero_fases: tensao_fase
    tipo_de_inversor: tipo_inversor
    numero_mppt: int | None = None


class InversorPublic(InversorSchema):
    id_inversor: int
    model_config = ConfigDict(from_attributes=True)


class InversorList(BaseModel):
    inversores: list[InversorPublic]
