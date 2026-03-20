from pydantic import BaseModel, ConfigDict, EmailStr
from api.schemas.cliente.endereco import EnderecoClientePublic, EnderecoObraPublic


class ClienteSchema(BaseModel):
    nome_cliente: str = "[NOME DO CLIENTE]"
    cpf: str = "[CPF DO CLIENTE]"
    data_nascimento: str = "[DATA DE NASCIMENTO DO CLIENTE]"
    razao_social: str | None = "RAZÃO SOCIAL DO CLIENTE"
    nome_fantasia: str | None = "NOME FANTASIA DO CLIENTE"
    cnpj: str | None = "[CNPJ DO CLIENTE]"
    rg: str = "[RG DO CLIENTE]"
    telefone_cliente: str = "[TELEFONE DO CLIENTE]"
    email_cliente: EmailStr = "email@cliente.br"

class ClientePublic(ClienteSchema):
    id_cliente: int
    user_id: int
    enderecos_cliente: list[EnderecoClientePublic] = []
    enderecos_obra: list[EnderecoObraPublic] = []
    model_config = ConfigDict(from_attributes=True)

class ClienteList(BaseModel):
    clientes: list[ClientePublic]

Cliente = ClienteSchema
