from pydantic import BaseModel, EmailStr

from api.schemas.cliente.endereco import EnderecoObra
from api.schemas.common.enums import classe_consumo, ramal_de_energia


class ProjetoFormularioEnelCe(BaseModel):
    numero_uc: str = "[INSIRA UC AQUI]"
    classe: classe_consumo
    ramal_energia: ramal_de_energia
    nome_cliente: str = "[NOME DO CLIENTE]"
    cpf: str = "CPF DO CLIENTE"
    telefone_cliente: str = "TELEFONE DO CLIENTE"
    email_cliente: str = "EMAIL CLIENTE"

    endereco_obra: EnderecoObra

    tensao_local: int = 220
    carga_instalada_kw: float = 8

    potencia_geracao: int = 8

    nome_procurador: str = "NOME DO PROCURADOR"
    cpf_procurador: str = "CPF DO PROCURADOR"
    email_procurador: EmailStr = "EMAIL@EMAIL.COM"
    data_hoje: str = "DD/MM/AAAA"
    telefone_procurador: str = "85 888888888"
