from dataclasses import dataclass, field
from src.schemas.models import tensao_fase, classe_consumo, ramal_de_energia, tipo_inversor


@dataclass
class Cliente():
    id_cliente: int | None = 1
    nome_cliente: str = "diego"
    cpf: str = "[CPF DO CLIENTE]"
    data_nascimento: str = "[DATA DE NASCIMENTO DO CLIENTE]"
    razao_social: str | None = "RAZÃO SOCIAL DO CLIENTE"
    nome_fantasia: str | None = "NOME FANTASIA DO CLIENTE"
    cnpj: str | None    = "[CNPJ DO CLIENTE]"
    rg: str = "[RG DO CLIENTE]"
    telefone_cliente: str = "[TELEFONE DO CLIENTE]"
    email_cliente: str = "email@cliente.br"

@dataclass
class EnderecoCliente():
    logradouro_cliente: str = "[LOGRADOURO DO CLIENTE]"
    numero_casa_cliente: str = "[NÚMERO DA CASA DO CLIENTE]"
    complemento_casa_cliente: str | None = " "
    cep_cliente: str = "[CEP DO CLIENTE]"
    bairro_cliente: str = "[BAIRRO DO CLIENTE]"
    cidade_cliente: str = "[CIDADE DO CLIENTE]"
    estado_cliente: str = "[ESTADO DO CLIENTE]"

@dataclass
class EnderecoObra():
    logradouro_obra: str = "[LOGRADOURO DA OBRA]"
    numero_obra: str = "[NÚMERO DA OBRA]"
    complemento_obra: str | None = " "
    cep_obra: str = "[CEP DA OBRA]"
    bairro_obra: str = "[BAIRRO DA OBRA]"
    cidade_obra: str = "[CIDADE DA OBRA]"
    estado_obra: str = "[ESTADO DA OBRA]"
    latitude_obra: str = "[NONE]"
    longitude_obra: str = "[NONE]"

@dataclass
class Projetista():
    id_projetista: int | None = None
    nome_projetista: str = "[NOME DO PROJETISTA]"
    creci_projetista: str = "[CRECI DO PROJETISTA]"
    rubrica_projetista: str = "[RUBRICA DO PROJETISTA]"
    telefone_projetista: str = "[TELEFONE DO PROJETISTA]"
    email_projetista: str = "email@projeto.br"

@dataclass
class Procurador():
    id_procurador: int | None = None
    nome_procurador: str = "[NOME DO PROCURADOR]"
    cpf_procurador: str = "[CPF DO PROCURADOR]"
    rg_procurador: str = "[RG DO PROCURADOR]"
    telefone_procurador: str = "[TELEFONE DO PROCURADOR]"
    email_procurador: str = "email@procurador.br"
    logradouro_procurador: str = "[LOGRADOURO DO PROCURADOR]"
    numero_casa_procurador: str = "[NÚMERO DA CASA DO PROCURADOR]"
    complemento_procurador: str | None = None
    cep_procurador: str = "[CEP DO PROCURADOR]"
    bairro_procurador: str = "[BAIRRO DO PROCURADOR]"
    cidade_procurador: str  = "[CIDADE DO PROCURADOR]"
    estado_procurador: str = "[ESTADO DO PROCURADOR]"

@dataclass
class QuantidadePlacas():
    quantidade_placas: int = 10
    quantidade_placas2: int | None = None

@dataclass
class Inversor():
    id_inversor: int | None
    marca_inversor: str = "[MARCA DO INVERSOR]"
    modelo_inversor: str = "[MODELO DO INVERSOR]"
    potencia_inversor: float =  0.0
    numero_fases: tensao_fase = "monofasico"
    tipo_de_inversor: tipo_inversor  = "string"
    numero_mppt: int | None = 4 #reservado para atualizações futuras

@dataclass
class Placa():
    id_placa: int | None = 1
    marca_placa: str = "[MARCA DA PLACA]"
    modelo_placa: str   = "[MODELO DA PLACA]"
    potencia_placa: float = 0.0
    tipo_celula: str = "[TIPO DE CÉLULA DA PLACA]"
    tensao_pico: float = 0.0
    corrente_curtocircuito: float = 0.0
    tensao_maxima_potencia: float = 0.0
    corrente_maxima_potencia: float = 0.0
    eficiencia_placa: float | None = 0.0 #reservado para atualizações futuras

@dataclass
class ConfiguracaoSistema():
    inversor: Inversor = field(default_factory=Inversor)
    quantidade_inversor: int = 1
    quantidade_total_placas_do_sistema: QuantidadePlacas = field(default_factory=QuantidadePlacas)
    placa: Placa = field(default_factory=Placa)
    placa2: Placa | None = None


@dataclass 
class ProjetoCompleto():
    id_projeto: int | None = 1
    
    numero_unidade_consumidora: str = "[NÚMERO DA UNIDADE CONSUMIDORA]"
    carga_instalada_kw: float = 10.0
    disjuntor_geral_amperes: float = 40.0
    energia_media_mensal_kwh: float = 200.0
    classe_consumo1: classe_consumo = classe_consumo.RESIDENCIAL
    tipo_fornecimento: tensao_fase = tensao_fase.MONOFASICO
    ramal_energia: ramal_de_energia = ramal_de_energia.AEREO
    data_projeto: str = "[DATA DO PROJETO]"
    quantidade_sistemas_instalados: int = 1

    cliente: Cliente = field(default_factory=Cliente)
    endereco_cliente : EnderecoCliente = field(default_factory=EnderecoCliente)
    endereco_obra : EnderecoObra = field(default_factory=EnderecoObra)
    projetista : Projetista = field(default_factory=Projetista)
    procurador : Procurador = field(default_factory=Procurador)
    
    sistema_instalado: list = field(default_factory=list[ConfiguracaoSistema])

    

    #quantidades de placas e inversores, por enquanto definidas pelo json de entrada.

@dataclass
class RetornoProjetoCompleto():
    #memorial descritivo
    #endereço da obra
    logradouro_obra: str | None = None
    numero_obra: str | None = None
    complemento_obra: str | None = None
    bairro_obra: str | None = None
    cidade_obra: str | None = None
    estado_obra: str | None = None
    cep_obra: str | None = None
    data_hoje: str | None = None
    data_futura: str | None = None
    latitude_obra: float | None = None
    longitude_obra: float | None = None
    
    #dados cliente
    nome_cliente: str | None = None
    cpf: str | None = None
    rg: str | None = None
    razao_social: str | None = None
    nome_fantasia: str | None = None 
    cnpj: str | None = None 
    telefone: str | None = None
    email: str | None = None
    data_nascimento: str | None = None 
    
    #dados elétricos do estabelecimento
    classe_consumo: str | None = None
    carga_instalada_kw: float | None = None
    energia_media_mensal_kwh: float | None = None
    tensao_local: int | None = None
    tipo_fornecimento: str | None = None
    disjuntor_geral: int | None = None
    numero_uc: str | None = None
    
    #textos do memorial descritivo
    texto_placas_memorial: str | None = None
    texto_inversor_memorial: str | None = None
    texto_potencia_placa: str | None = None
    texto_tensao_individual_paineis: str | None = None
    texto_protecao_inversor: str | None = None
    gerador_texto_introducao: str | None = None
    gerador_texto_introducao2: str | None = None
    texto_cabos: list[str] | None = None
    texto_2_protecao_inversor: list[int] | None = None
    texto_corrente_max_cabo: str | None = None
    
    #dados painel
    tipo_celula: str | None = None
    quantidade_final_placas: int | None = None
    potencia_total_paineis_final: float | None = None
    
    #dados inversor
    numero_total_strings: int | None = None
    quantidade_final_de_placas_por_inversor: list[int] | None = None
    potencia_inversores: list[float] | None = None
    corrente_saida_por_inversor: list[float] | None = None

    #####
    potencia_efetiva: float | None = None
    energia_gerada_mensal: float | None = None
    queda_tensao: float | None = None

    #dados projetista
    projetista: str | None = None
    cft_crea: str | None = None
    #
    equacao: str | None = None
    equacao2: str | None = None
    equacao3: str | None = None
    equacao4: str | None = None
    
@dataclass
class RetornoProjetoDiagrama():
    #memorial descritivo
    #endereço da obra
    logradouro_obra: str | None = None
    numero_obra: str | None = None
    complemento_obra: str | None = None
    bairro_obra: str | None = None
    cidade_obra: str | None = None
    estado_obra: str | None = None
    cep_obra: str | None = None
    data_hoje: str | None = None
    data_futura: str | None = None
    latitude_obra: float | None = None
    longitude_obra: float | None = None

    