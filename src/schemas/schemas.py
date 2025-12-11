from pydantic import BaseModel, EmailStr

from src.schemas.models import tensao_fase, classe_consumo, ramal_energia, tipo_inversor


class Cliente(BaseModel):
    id_cliente: int | None = None
    nome_cliente: str = "[NOME DO CLIENTE]"
    cpf: str = "[CPF DO CLIENTE]"
    data_nascimento: str = "[DATA DE NASCIMENTO DO CLIENTE]"
    razao_social: str | None = "RAZÃO SOCIAL DO CLIENTE"
    nome_fantasia: str | None = "NOME FANTASIA DO CLIENTE"
    cnpj: str | None    = "[CNPJ DO CLIENTE]"
    rg: str = "[RG DO CLIENTE]"
    telefone_cliente: str = "[TELEFONE DO CLIENTE]"
    email_cliente: EmailStr = "email@cliente.br"

class EnderecoCliente(BaseModel):
    logradouro_cliente: str = "[LOGRADOURO DO CLIENTE]"
    numero_casa_cliente: str = "[NÚMERO DA CASA DO CLIENTE]"
    complemento_casa_cliente: str | None = None
    cep_cliente: str = "[CEP DO CLIENTE]"
    bairro_cliente: str = "[BAIRRO DO CLIENTE]"
    cidade_cliente: str = "[CIDADE DO CLIENTE]"
    estado_cliente: str = "[ESTADO DO CLIENTE]"

class EnderecoObra(BaseModel):
    logradouro_obra: str = "[LOGRADOURO DA OBRA]"
    numero_obra: str = "[NÚMERO DA OBRA]"
    complemento_obra: str | None = None
    cep_obra: str = "[CEP DA OBRA]"
    bairro_obra: str = "[BAIRRO DA OBRA]"
    cidade_obra: str = "[CIDADE DA OBRA]"
    estado_obra: str = "[ESTADO DA OBRA]"
    latitude_obra: str | None = None
    longitude_obra: str | None = None

class Inversor(BaseModel):
    id_inversor: int | None
    marca_inversor: str = "[MARCA DO INVERSOR]"
    modelo_inversor: str = "[MODELO DO INVERSOR]"
    potencia_inversor: float =  0.0
    numero_fases: tensao_fase = "monofasico"
    tipo_de_inversor: tipo_inversor  = "string"
    numero_mppt: int | None = 4 #reservado para atualizações futuras

    

class Placa(BaseModel):
    id_placa: int | None
    marca_placa: str = "[MARCA DA PLACA]"
    modelo_placa: str   = "[MODELO DA PLACA]"
    potencia_placa: float = 0.0
    tipo_celula: str = "[TIPO DE CÉLULA DA PLACA]"
    tensao_pico: float = 0.0
    corrente_curtocircuito: float = 0.0
    tensao_maxima_potencia: float = 0.0
    corrente_maxima_potencia: float = 0.0
    eficiencia_placa: float | None #reservado para atualizações futuras

class Projetista(BaseModel):
    id_projetista: int | None = None
    nome_projetista: str = "[NOME DO PROJETISTA]"
    creci_projetista: str = "[CRECI DO PROJETISTA]"
    rubrica_projetista: str = "[RUBRICA DO PROJETISTA]"
    telefone_projetista: str = "[TELEFONE DO PROJETISTA]"
    email_projetista: EmailStr = "email@projeto.br"

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
    cidade_procurador: str  = "[CIDADE DO PROCURADOR]"
    estado_procurador: str = "[ESTADO DO PROCURADOR]"


class QuantidadePlacas(BaseModel):
    quantidade_placas: int
    quantidade_placas2: int | None = None

class ConfiguracaoSistema(BaseModel):
    inversor: Inversor
    quantidade_inversor: int = 1
    quantidade_total_placas_do_sistema: QuantidadePlacas
    placa: Placa
    placa2: Placa | None = None

 
class Projeto(BaseModel):
    model_config = {"use_enum_values": True}
    id_projeto: int | None
    
    numero_unidade_consumidora: str
    carga_instalada_kw: float = 10.0
    disjuntor_geral_amperes: float = 40.0
    energia_media_mensal_kwh: float = 200.0
    classe_consumo:  classe_consumo #residencial, comercial, industrial, rural
    tipo_fornecimento: tensao_fase #monofasico, bifasico, trifasico
    ramal_energia: ramal_energia #aéreo, subterrâneo
    data_projeto: str
    quantidade_sistemas_instalados: int = 1
    cliente: Cliente
    endereco_cliente: EnderecoCliente
    endereco_obra: EnderecoObra
    projetista: Projetista
    procurador: Procurador

    sistema_instalado: list[ConfiguracaoSistema]
    #quantidades de placas e inversores, por enquanto definidas pelo json de entrada.

class ProjetoTeste(BaseModel):
    model_config = {"use_enum_values": True}
    id_projeto: int | None
    numero_unidade_consumidora: str
    carga_instalada_kw: float = 10.0
    disjuntor_geral_amperes: float = 40.0
    energia_media_mensal_kwh: float = 200.0
    classe_consumo:  classe_consumo #residencial, comercial, industrial, rural
    tipo_fornecimento: tensao_fase #monofasico, bifasico, trifasico
    ramal_energia: ramal_energia #aéreo, subterrâneo
    data_projeto: str

    quantidade_sistemas_instalados: int = 1