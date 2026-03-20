from pydantic import BaseModel, ConfigDict


class EnderecoClienteSchema(BaseModel):
    logradouro_cliente: str = "[LOGRADOURO DO CLIENTE]"
    numero_casa_cliente: str = "[NÚMERO DA CASA DO CLIENTE]"
    complemento_casa_cliente: str | None = None
    cep_cliente: str = "[CEP DO CLIENTE]"
    bairro_cliente: str = "[BAIRRO DO CLIENTE]"
    cidade_cliente: str = "[CIDADE DO CLIENTE]"
    estado_cliente: str = "[ESTADO DO CLIENTE]"

class EnderecoClientePublic(EnderecoClienteSchema):
    id_endereco_cliente: int
    cliente_id: int
    model_config = ConfigDict(from_attributes=True)


class EnderecoObraSchema(BaseModel):
    logradouro_obra: str = "[LOGRADOURO DA OBRA]"
    numero_obra: str = "[NÚMERO DA OBRA]"
    complemento_obra: str | None = None
    cep_obra: str = "[CEP DA OBRA]"
    bairro_obra: str = "[BAIRRO DA OBRA]"
    cidade_obra: str = "[CIDADE DA OBRA]"
    estado_obra: str = "[ESTADO DA OBRA]"
    latitude_obra: str | None = None
    longitude_obra: str | None = None

class EnderecoObraPublic(EnderecoObraSchema):
    id_endereco_obra: int
    cliente_id: int
    model_config = ConfigDict(from_attributes=True)

EnderecoCliente = EnderecoClienteSchema
EnderecoObra = EnderecoObraSchema
