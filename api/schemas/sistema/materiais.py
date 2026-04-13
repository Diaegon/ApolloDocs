from pydantic import BaseModel
from api.schemas.sistema.inversor import Inversor
from api.schemas.sistema.placas import Placa


class MaterialInversor(BaseModel):
    inversor: Inversor
    quantidade: int = 1


class MaterialPlaca(BaseModel):
    placa: Placa
    quantidade: int = 10


class MaterialInversorRef(BaseModel):
    """ID-based reference used by the v2 API endpoint."""
    id_inversor: int
    quantidade: int = 1


class MaterialPlacaRef(BaseModel):
    """ID-based reference used by the v2 API endpoint."""
    id_placa: int
    quantidade: int = 10
