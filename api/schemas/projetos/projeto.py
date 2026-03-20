from pydantic import BaseModel, ConfigDict
from api.schemas.cliente.cliente import ClientePublic
from api.schemas.pessoas.procurador import ProcuradorPublic

class ProjetoSchema(BaseModel):
    cliente_id: int
    procurador_id: int
    projetista_id: int | None = None
    inversor_1_id: int | None = None
    inversor_2_id: int | None = None
    inversor_3_id: int | None = None
    placa_1_id: int | None = None
    placa_2_id: int | None = None
    placa_3_id: int | None = None

class ProjetoPublic(ProjetoSchema):
    id_projeto: int
    user_id: int
    cliente: ClientePublic | None = None
    procurador: ProcuradorPublic | None = None
    model_config = ConfigDict(from_attributes=True)

class ProjetoList(BaseModel):
    projetos: list[ProjetoPublic]
