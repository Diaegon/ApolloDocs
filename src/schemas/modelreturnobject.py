from dataclasses import dataclass, field
from src.schemas.models import tensao_fase, classe_consumo, ramal_de_energia, tipo_inversor


@dataclass(init=False)
class Cliente():
    id_cliente: int = 1 
    nome_cliente: str 
    cpf: str
    data_nascimento: str 
    razao_social: str 
    nome_fantasia: str
    cnpj: str 
    rg: str 
    telefone_cliente: str
    email_cliente: str

@dataclass
class EnderecoCliente():
    logradouro_cliente: str 
    numero_casa_cliente: str 
    complemento_casa_cliente: str 
    cep_cliente: str 
    bairro_cliente: str 
    cidade_cliente: str 
    estado_cliente: str 

@dataclass
class EnderecoObra():
    logradouro_obra: str 
    numero_obra: str 
    complemento_obra: str
    cep_obra: str 
    bairro_obra: str 
    cidade_obra: str
    estado_obra: str 
    latitude_obra: str
    longitude_obra: str

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


@dataclass() 
class ProjetoCompleto():
    id_projeto: int 
    
    numero_unidade_consumidora: str 
    carga_instalada_kw: float 
    disjuntor_geral_amperes: float 
    energia_media_mensal_kwh: float 
    classe_consumo1: classe_consumo 
    tipo_fornecimento: tensao_fase 
    ramal_energia: ramal_de_energia
    data_projeto: str 
    quantidade_sistemas_instalados: int 

    cliente: Cliente
    endereco_obra : EnderecoObra 
 
    
    sistema_instalado: list 

    

    #quantidades de placas e inversores, por enquanto definidas pelo json de entrada.

@dataclass()
class RetornoProjetoCompleto():
    #memorial descritivo
    #endereço da obra
    logradouro_obra: str 
    numero_obra: str 
    complemento_obra: str 
    bairro_obra: str 
    cidade_obra: str 
    estado_obra: str 
    cep_obra: str 
    data_hoje: str 
    data_futura: str 
    latitude_obra: float 
    longitude_obra: float 
    
    #dados cliente
    nome_cliente: str 
    cpf: str 
    rg: str 
    razao_social: str 
    nome_fantasia: str  
    cnpj: str  
    telefone: str 
    email: str 
    data_nascimento: str  
    
    #dados elétricos do estabelecimento
    classe_consumo: str 
    carga_instalada_kw: float 
    energia_media_mensal_kwh: float 
    tensao_local: int 
    tipo_fornecimento: str 
    disjuntor_geral: int 
    numero_uc: str 
    
    #textos do memorial descritivo
    texto_placas_memorial: str 
    texto_inversor_memorial: str 
    texto_potencia_placa: str 
    texto_tensao_individual_paineis: str 
    texto_protecao_inversor: str 
    gerador_texto_introducao: str 
    gerador_texto_introducao2: str 
    texto_cabos: list[str] 
    texto_2_protecao_inversor: list[int] 
    texto_corrente_max_cabo: str 
    
    #dados painel
    tipo_celula: str 
    quantidade_final_placas: int 
    potencia_total_paineis_final: float 
    corrente_mp: float
    corrente_cc: float
    tensao_circuito_aberto: float

    #dados inversor
    numero_total_strings: int 
    quantidade_final_de_placas_por_inversor: list[int] 
    potencia_inversores: list[float] 
    corrente_saida_por_inversor: list[float] 
    inversor_tensao: list[float]
    #####
    potencia_efetiva: float 
    energia_gerada_mensal: float 
    queda_tensao: float 

    #
    equacao: str 
    equacao2: str 
    equacao3: str 
    equacao4: str 
    
@dataclass
class RetornoProjetoDiagrama():
    #memorial descritivo
    #endereço da obra
    logradouro_obra: str  = None
    numero_obra: str  = None
    complemento_obra: str  = None
    bairro_obra: str  = None
    cidade_obra: str  = None
    estado_obra: str  = None
    cep_obra: str  = None
    data_hoje: str  = None
    data_futura: str  = None
    latitude_obra: float  = None
    longitude_obra: float  = None

    