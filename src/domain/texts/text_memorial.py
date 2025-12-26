class TextoMemorial:  # noqa: PLR0904
    def __init__(self, retorno):
        self.retorno = retorno
        pass

    def texto_introducao(self):

        texto_inicial = f"   O presente relatório técnico tem por objetivo apresentar o memorial descritivo \
                        para implantação de um Gerador Fotovoltaico de fabricação <b>{self.retorno.gerador_texto_introducao}, {self.retorno.gerador_texto_introducao2}</b>. \
                            Este modelo e quantidade de gerador foi previamente aprovado pelo proprietário da residência.\
                                Este gerador fotovoltaico se conectará ao sistema de baixa tensão, após a medição \
                                    de energia da ENEL. O mesmo terá como objetivo suprir parte das cargas desta residencia. \
                                    A previsão de ligação do sistema elétrico é para <b>{self.retorno.data_futura}</b>."

        return texto_inicial

    def texto_loc(self):
        return f"No diagrama de situação é ilustrada a planta de situação da residência onde será \
    implantado na {self.retorno.logradouro_obra}, {self.retorno.numero_obra} \
            {self.retorno.complemento_obra}, {self.retorno.cidade_obra}, {self.retorno.estado_obra}. A tabela 2.1 \
    mostra o georeferenciamento da localidade de instalação e do gerador."

    @staticmethod
    def texto_loc2():
        return (
            "A área de telhado do local de isntalação foi escolhida por apresentar vantagens de insolação \
    permanente durante todas as horas do dia para evitar o sombreamento dos painéis \
    fotovoltaicos e segurança dos equipamentos"
        )

    def texto_carginst(self):
        return f"A carga instalada é típica de um estabelecimento {self.retorno.classe_consumo}, constituído de iluminação e \
    eletroeletrônicos diversos, sendo {self.retorno.carga_instalada_kw} kW.  A energia \
    media de consumo é de  {self.retorno.energia_media_mensal_kwh} kWh."

    @staticmethod
    def texto_calculo_demanda():
        return (
            "Considerando um mês comercial com 720 horas, pode-se calcular a demanda média \
    mensal através da equação:"
        )

    @staticmethod
    def texto_calculo_demanda2():
        return (
            "Esta demanda média está dentro do limite da potência máxima injetada no sistema \
    da ENEL, de acordo com a norma NT - 010."
        )

    @staticmethod
    def texto_calculo_fc():
        return "O fator de carga médio desta residência é calculado através da equação:"

    def texto_geradorfv(self):
        texto_retorno = f"O Gerador Fotovoltaico escolhido para compor a geração suplementar da residência \
    Alvo deste projeto é composto de {self.retorno.texto_placas_memorial} e {self.retorno.texto_inversor_memorial}. \
    O   modulo   solar   fotovoltaico   {self.retorno.tipo_celula}  possui   as   características \
    técnicas   apresentado   na   tabela   a seguir.   Considerando   que   os   módulos   instalados   são   os   de \
    ({self.retorno.texto_potencia_placa})  Wp, e que eles tem uma tensão elétrica de máxima potência (Vmp) de ({self.retorno.texto_tensao_individual_paineis})Vmp. A \
    solução prevista para ser instalada tem {self.retorno.numero_total_strings} arranjos dispostos da seguinte maneira{self.retorno.quantidade_final_de_placas_por_inversor}, totalizando \
    {self.retorno.quantidade_final_placas} módulos que resultam numa potência total de {self.retorno.potencia_total_paineis_final} kWp."

        return f"{texto_retorno}"

    def texto_potenciafv(self):
        texto_retorno = f"O georeferenciamento do local da instalação do Gerador Fotovoltaico estabelece o \
        valor de 74,5% das Condições de Teste padrão (STC) do modulo Fotovoltaico. Por essa \
        premissa,  terei   uma   Potencia   resultante   do  meu  Gerador  Fotovoltaico  (GF)  também   de \
        74,5% da Potencia instalada ({self.retorno.potencia_total_paineis_final} kW). Assim, a Potencia efetiva \
        do GF é de  {self.retorno.potencia_efetiva}kW, o\
        que satisfaz a demanda média calculada."

        return texto_retorno

    def texto_calculo_enegiagerada(self):
        return f"Considerando a potência média disponível de  {self.retorno.potencia_efetiva} kW  e a média anual do ponto \
    georeferenciado do sistema Horas de Sol a Pico (HSP) que é de 5,84 kWh/m2/dia, como \
    parâmetro de medição da radiação solar em um mês comercial, pode-se calcular a energia \
    média através do produto destas duas grandezas, que resulta em {self.retorno.energia_gerada_mensal} kWh."

    @staticmethod
    def texto_diagramas():
        return (
            "A figura a seguir apresenta o esquema básico de ligação de um Gerador Fotovoltaico. \
    Nesta   figura   pode   ser   ver   todas   as   partes   que   compõem   o   sistema,   desde   o   Gerador \
    Fotovoltaico até a conexão à carga e à rede."
        )

    @staticmethod
    def texto_parametrizacao():
        return "O inversor para cumprir sua função de proteção, é parametrizado com os seguintes \
    valores, de modo a não exceder os limites recomendados pela norma NT – 010 Coelce."

    def texto_instalacao(self):
        return f"A Localidade é alimentada através da rede de baixa tensão da ENEL em {self.retorno.tensao_local}V. O \
    ponto de entrega se dá em um quadro instalado junto ao muro da propriedade."

    @staticmethod
    def texto_diagramauni():
        return "O diagrama unifilar geral se encontra em anexo."

    def texto_dimensionamento_protecao(self):
        return f"Este   Gerador   Fotovoltaico   será   conectado   ao   barramento   de   baixa   tensão   do \
    consumidor, logo abaixo da proteção geral, que é constituída por um disjuntor {self.retorno.tipo_fornecimento} \
    de {self.retorno.disjuntor_geral}   A.   Por   sua   vez,   o   ramal   de   interligação do Gerador Fotovoltaico ao quadro de \
    medição é feito por  {self.retorno.texto_protecao_inversor} Esta capacidade de condução foi \
    calculada através da seguinte equação."

    def texto_dimensionamento_protecao2(self):
        return f"A interligação entre o Gerador Fotovoltaico {self.retorno.potencia_inversores} W e o quadro de medição será feito através \
    de um cabo de cobre flexível, isolado em PVC com uma seção reta de {self.retorno.texto_cabos}, respectivamente e sua \
    proteção se dará através de disjuntor de {self.retorno.texto_2_protecao_inversor} A. \
    O   dimensionamento   do   condutor   de   {self.retorno.texto_cabos}   atende   aos   critérios   de   máxima \
    capacidade de corrente, já que o mesmo tem capacidade térmica de conduzir até {self.retorno.texto_corrente_max_cabo} e \
    atende também ao critério de máxima queda de tensão. \
    Como trata-se da interligação de um gerador, a máxima queda de tensão permitida é \
    de 3%. A equação abaixo apresenta o cálculo desta queda."

    def texto_dimensionamento_protecao3(self):
        return f"Introduzindo estes valores na equação anterior resulta em uma queda de tensão de {self.retorno.queda_tensao} , o que satisfaz plenamente o limite máximo de queda que é de 3%."

    def texto_disjuntores(self):
        return f"A proteção geral é feita através de um disjuntor {self.retorno.tipo_fornecimento} de {self.retorno.disjuntor_geral} A, com curva \
    direta de atuação C, e o Gerador Fotovoltaico terá a sua proteção realizada por  \
    {self.retorno.texto_protecao_inversor}, curva de atuação B. A seletividade é garantida observando o valor \
    maior de corrente nominal do disjuntor principal em relação ao disjuntor para proteção do \
    cabo do inversor, e suas curvas de atuação."

    @staticmethod
    def texto_sinalizacao():
        return (
            "No padrão de entrada será instalada placa de sinalização, confeccionada em \
    PVC 2,0 mm com tratamento anti-UV, conforme Figura a seguir, fixada de acordo \
    com o desenho D010.01 dá NT Br-010 R-01, sem que haja a perfuração da caixa para \
    fixação da sinalização. "
        )

    def texto_data(self):
        return f"{self.retorno.data_hoje}"
