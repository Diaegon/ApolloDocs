from pydantic import BaseModel, EmailStr


class Procurador(BaseModel):
    id_procurador: int | None = None
    nome_procurador: str = "[NOME DO PROCURADOR]"
    cpf_procurador: str = "[CPF DO PROCURADOR]"
    rg_procurador: str = "[RG DO PROCURADOR]"
    telefone_procurador: str = "[TELEFONE DO PROCURADOR]"
    email_procurador: EmailStr = "email@procurador.br"
    logradouro_procurador: str = "[LOGRADOURO DO PROCURADOR]"
    numero_casa_procurador: str = "[NÚMERO DA CASA DO PROCURADOR]"
    complemento_procurador: str | None = None
    cep_procurador: str = "[CEP DO PROCURADOR]"
    bairro_procurador: str = "[BAIRRO DO PROCURADOR]"
    cidade_procurador: str = "[CIDADE DO PROCURADOR]"
    estado_procurador: str = "[ESTADO DO PROCURADOR]"
