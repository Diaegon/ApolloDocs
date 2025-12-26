from pydantic import BaseModel, EmailStr


class Cliente(BaseModel):
    id_cliente: int | None = None
    nome_cliente: str = "[NOME DO CLIENTE]"
    cpf: str = "[CPF DO CLIENTE]"
    data_nascimento: str = "[DATA DE NASCIMENTO DO CLIENTE]"
    razao_social: str | None = "RAZÃO SOCIAL DO CLIENTE"
    nome_fantasia: str | None = "NOME FANTASIA DO CLIENTE"
    cnpj: str | None = "[CNPJ DO CLIENTE]"
    rg: str = "[RG DO CLIENTE]"
    telefone_cliente: str = "[TELEFONE DO CLIENTE]"
    email_cliente: EmailStr = "email@cliente.br"
