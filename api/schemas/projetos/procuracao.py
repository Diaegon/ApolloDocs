from pydantic import BaseModel

from api.schemas.cliente.cliente import Cliente
from api.schemas.cliente.endereco import EnderecoCliente, EnderecoObra
from api.schemas.pessoas.procurador import Procurador


class ProjetoProcuracao(BaseModel):
    model_config = {"use_enum_values": True}
    id_projeto: int | None

    cliente: Cliente
    endereco_cliente: EnderecoCliente
    endereco_obra: EnderecoObra
    procurador: Procurador
