from dataclasses import dataclass

@dataclass
class RetornoObjetosCalculados():
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
    

