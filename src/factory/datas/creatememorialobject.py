#por enquanto objeto está aqui, mas o ideal é isntanciar de outro lugar
from src.factory.datas.utils.calculos import Calculos
from src.schemas.modelreturnobject import RetornoProjetoCompleto, ProjetoCompleto
from datetime import datetime
from dateutil.relativedelta import relativedelta
import locale
import pprint

try:
    locale.setlocale(locale.LC_TIME, "pt_BR.utf8")
except:
    # fallback seguro para servidores como o Render
    locale.setlocale(locale.LC_TIME, "C")
    
class ObjetosCalculados(Calculos):
    def __init__(self, projeto):
        #check
        self.projeto = projeto
        self.numero_total_strings = 0
        self.quantidade_sistemas = 0
        self.multiplicador = []
        self.inversor_tensao = []
        self.quantidade_final_placas = 0
        self.potencia_total_paineis_final = 0
        self.quantidade_final_de_placas_por_inversor = []
        self.texto_placas_memorial = "" 
        self.texto_inversor_memorial = ""
        self.texto_potencia_placa = ""
        self.texto_tensao_individual_paineis = ""
        self.texto_tensao_circuito_aberto = ""
        self.corrente_maxima_potencia = ""
        self.corrente_cc = ""
        self.texto_protecao_inversor = ""
        self.texto_corrente_max_cabo = ""
        self.texto_cabos = []
        self.texto_2_protecao_inversor = []
        self.potencia_inversores = []
        self.potencia_total_inversores_final = 0
        self.tensao_queda = []
        self.corrente_saida_por_inversor =[]
        self.gerador_texto_introducao2 = ""
        self.lista_equacoes_protecao_inversores = []
        self.checagem_sistemas_instalados()
        self.checagem_inversores()
        self.checagem_placas()
        self.calculo_disposicao_placas()
        #retorno


    def checagem_sistemas_instalados(self):
        sistemas_instalados = self.projeto.sistema_instalado
        self.quantidade_sistemas = len(sistemas_instalados)
    
    def get_multiplicador(self, sistema, numero_fases) -> float:
        """Retorna o multiplicador baseado no número de fases."""
        numero_fases = self.projeto.sistema_instalado[sistema].inversor.numero_fases
        if numero_fases == 'monofasico':
            self.multiplicador.append(1)
            self.inversor_tensao.append(220)
        elif numero_fases == 'trifasico':
            self.multiplicador.append(1.732)
            self.inversor_tensao.append(380)
        else:
            raise ValueError("Número de fases do inversor inválido")

    def get_classe_codigo(self):
        classe_cliente = self.projeto.classe_consumo
        if classe_cliente == "residencial":
            classe_codigo = "B1"
        elif classe_cliente == "rural":
            classe_codigo = "B2"
        elif classe_cliente == "comercial":
            classe_codigo = "B3"

        return classe_codigo

    def get_tensao_local(self):
        tensao_cliente = self.projeto.tipo_fornecimento
        if tensao_cliente == "monofasico":
            tensao_local = 220
        elif tensao_cliente == "bifasico":
            tensao_local = 220
        elif tensao_cliente == "trifasico":
            tensao_local = 380

        return tensao_local
    
    def checagem_inversores(self):
        marca_de_inversores = []
        modelo_inversores = []

        for sistema in range(self.quantidade_sistemas):
            quantidade_inversor = self.projeto.sistema_instalado[sistema].quantidade_inversor
            marca_de_inversores.append(self.projeto.sistema_instalado[sistema].inversor.marca_inversor)
            modelo_inversores = self.projeto.sistema_instalado[sistema].inversor.modelo_inversor
            potencia_inversor = self.projeto.sistema_instalado[sistema].inversor.potencia_inversor
            numero_fases = self.projeto.sistema_instalado[sistema].inversor.numero_fases
            
            self.get_multiplicador(sistema, numero_fases)
            corrente_saida_inversor = round(self.get_corrente_saida(potencia_inversor, self.multiplicador[sistema], self.inversor_tensao[sistema]),2)
            self.corrente_saida_por_inversor.append(corrente_saida_inversor)
            cabo = self.cabo_energia_inversor(corrente_saida_inversor)
            cabo_inteiro = int(cabo.split()[0])
            
            self.potencia_inversores.append(potencia_inversor)
            queda_tensao = self.calculo_queda_tensao(int(corrente_saida_inversor),
                                                     int(self.inversor_tensao[sistema]),
                                                       cabo_inteiro)
            self.tensao_queda.append(queda_tensao)
            disjuntor_protecao = self.disjuntor_protecao(corrente_saida_inversor)

            self.texto_cabos.append(cabo)
            self.texto_2_protecao_inversor.append(disjuntor_protecao)
            self.texto_protecao_inversor += f" {quantidade_inversor} disjuntor de {disjuntor_protecao} A,"
            self.texto_corrente_max_cabo += self.corrente_max_cabo(corrente_saida_inversor) + ","
            self.texto_inversor_memorial += f" {quantidade_inversor} inversor {marca_de_inversores[-1]} {modelo_inversores}," 
            self.gerador_texto_introducao2 += f"{modelo_inversores} "
            
        for marca in marca_de_inversores:
            if marca_de_inversores.count(marca) > 1:
                marca_de_inversores.remove(marca)
        self.gerador_texto_introducao = ', '.join(marca_de_inversores)        

    def checagem_placas(self):
        
        def monta_texto_placa(item):

            quantidade_placas = list(self.projeto.sistema_instalado[item].quantidade_total_placas_do_sistema.model_dump().values())
            marca_placas = str(self.projeto.sistema_instalado[item].placa.marca_placa)
            modelo_placas = str(self.projeto.sistema_instalado[item].placa.modelo_placa)
            potencia_placa = str(self.projeto.sistema_instalado[item].placa.potencia_placa)
            tensao_individual = str(self.projeto.sistema_instalado[item].placa.tensao_maxima_potencia)
            tensao_circuito_aberto = str(self.projeto.sistema_instalado[item].placa.tensao_pico)
            corrente_maxima_potencia = str(self.projeto.sistema_instalado[item].placa.corrente_maxima_potencia)
            corrente_cc = str(self.projeto.sistema_instalado[item].placa.corrente_curtocircuito)
            self.texto_tensao_individual_paineis += f" {tensao_individual},"
            self.texto_potencia_placa += f" {potencia_placa},"
            self.texto_tensao_circuito_aberto +=  f" {tensao_circuito_aberto},"
            self.corrente_maxima_potencia += f" {corrente_maxima_potencia},"
            self.corrente_cc += f" {corrente_cc},"
            texto_por_placa = f" {quantidade_placas[0]} modulos  {marca_placas} {modelo_placas}, de {potencia_placa}Wp" 
            
            return texto_por_placa
        
        def monta_texto_placa2(item):

            quantidade_placas2 = list(self.projeto.sistema_instalado[item].quantidade_total_placas_do_sistema.model_dump().values())
            marca_placas2 = str(self.projeto.sistema_instalado[item].placa2.marca_placa)
            modelo_placas2 = str(self.projeto.sistema_instalado[item].placa2.modelo_placa)
            potencia_placa2 = str(self.projeto.sistema_instalado[item].placa2.potencia_placa)
            tensao_individual2 = str(self.projeto.sistema_instalado[item].placa2.tensao_maxima_potencia)
            tensao_circuito_aberto2 = str(self.projeto.sistema_instalado[item].placa2.tensao_pico)
            corrente_maxima_potencia2 = str(self.projeto.sistema_instalado[item].placa2.corrente_maxima_potencia)
            corrente_cc2 = str(self.projeto.sistema_instalado[item].placa2.corrente_curtocircuito)
            self.texto_tensao_individual_paineis += f" {tensao_individual2},"
            self.texto_potencia_placa += f" {potencia_placa2},"
            self.texto_tensao_circuito_aberto +=  f" {tensao_circuito_aberto2},"
            self.corrente_maxima_potencia += f" {corrente_maxima_potencia2},"
            self.corrente_cc += f" {corrente_cc2},"
            texto_por_placa2 = f" {quantidade_placas2[1]}  modulos {marca_placas2} {modelo_placas2}, de {potencia_placa2}Wp"

            return texto_por_placa2
        
        for item in range(self.quantidade_sistemas):
            sistemas_instalados = self.projeto.sistema_instalado[item]
            quantidade_placas_lista = quantidade_placas_lista = list(sistemas_instalados.quantidade_total_placas_do_sistema.model_dump().values())

            texto_da_placa = monta_texto_placa(item)
            self.texto_placas_memorial += texto_da_placa
            if quantidade_placas_lista[1]:
                texto_da_placa2 = monta_texto_placa2(item)
                self.texto_placas_memorial += texto_da_placa2
    #conta a quantidade de placas de um sistema considerando que um sistema só vai ter no máximo dois tipos de placa.
    def conta_placa_do_sistema(self,i):
        sistemas_instalados = self.projeto.sistema_instalado[i]
        quantidade_final = []
        #debug
        quantidade_placas_lista = list(sistemas_instalados.quantidade_total_placas_do_sistema.model_dump().values())

        quantidade_placa1 = quantidade_placas_lista[0] 
        modelo = sistemas_instalados.placa.modelo_placa
        marca = sistemas_instalados.placa.marca_placa
        potencia = sistemas_instalados.placa.potencia_placa
        quantidade_ = [modelo, marca, potencia,quantidade_placa1]
        quantidade_final.append(quantidade_)
        self.quantidade_final_placas += quantidade_placa1 
        
        #monta a lista
        #  
        if quantidade_placas_lista[1] not in [None, 0]:
            quantidade_placa2 = quantidade_placas_lista[1]
            modelo2 =  sistemas_instalados.placa2.modelo_placa
            marca2 = sistemas_instalados.placa2.marca_placa
            potencia2 = sistemas_instalados.placa2.potencia_placa
            quantidade_2 = [modelo2, marca2, potencia2,quantidade_placa2]
            quantidade_final.append(quantidade_2) 
            self.quantidade_final_placas += quantidade_placa2
        
        
        return quantidade_final
    #calcula a distribuição das placas no inversor, como nesse self.projeto cada sistema só tem um inversor, fica mais simples o calculo
    #vamos deixar a resposta crua sem identificar quais placas vão ser arranjadas;
    def distribui_placa_por_inversor(self,quantidade_sistemas):
        numero_strings = self.projeto.sistema_instalado[quantidade_sistemas].inversor.numero_mppt
        self.numero_total_strings += numero_strings
        placas_sistema = self.conta_placa_do_sistema(quantidade_sistemas)
        numero_painel1 = placas_sistema[0][3]
        self.potencia_total_paineis_final += (placas_sistema[0][3] * placas_sistema[0][2]) / 1000
        numero_de_paineis = numero_painel1
        if len(placas_sistema) > 1 and placas_sistema[1][3] not in [None, 0]:
            numero_painel2 = placas_sistema[1][3]
            self.potencia_total_paineis_final += (placas_sistema[1][3] * placas_sistema[1][2]) / 1000
            numero_de_paineis += numero_painel2

        lista_string = []

        resto_placas_por_string = numero_de_paineis % numero_strings
        placas_por_string = numero_de_paineis // numero_strings
        for numero_mppt in range(numero_strings):
            lista_string.append(placas_por_string)
        if resto_placas_por_string != 0:
            lista_string[-1] += resto_placas_por_string
        return lista_string

    #aqui iteramos sobre cada sistema instalado
    def calculo_disposicao_placas(self):  
        for quantidade_sistemas in range(self.projeto.quantidade_sistemas_instalados):
            quantidade_de_placas_por_inversor = self.distribui_placa_por_inversor(quantidade_sistemas)
            self.quantidade_final_de_placas_por_inversor.append(quantidade_de_placas_por_inversor)
        #retornamos a quantidade final de placas caso tenha mais de um sistema instalado.

    def data_de_hoje(self):
        data_de_hoje = datetime.now()
        # data_futura = data_de_hoje+relativedelta(months=1)
        # locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
        # plt.rcParams['text.usetex'] = True # Ativar o uso do LaTeX real (MikTeX)
        return data_de_hoje
    
    def data_futura(data_de_hoje):
        data_futura = data_de_hoje+relativedelta(months=1)
        data_futura = data_futura.strftime("%d de %B de %Y")
        return data_futura
    
    def equacao_demanda(self):
        resultado = self.projeto.energia_media_mensal_kwh / 720
        equacao = fr"$D_{{\mathrm{{media}}}} = \frac{{\mathrm{{Energia\ media}}}}{{N^{{\circ}}\,\mathrm{{de\ horas}}}} = \frac{{{self.projeto.energia_media_mensal_kwh}}}{{720}} = {resultado:.2f}\ kW$"
        return equacao
    
    
    def calculo_fator_de_carga(self):
        fatordecarga = (self.projeto.energia_media_mensal_kwh / 720) / self.projeto.carga_instalada_kw
        equacao2 = fr"$FC = \frac{{\mathrm{{Energia}}}}{{\mathrm{{Potencia \ instalada \ x \ 720h}}}} = \frac{{{self.projeto.energia_media_mensal_kwh}}}{{{self.projeto.carga_instalada_kw} \ x  \ 720}} = {fatordecarga:.2f}\ kW$"
        return equacao2    
    
    def conta_equacoes_inversor(self):
        equacao = []
        for sistema in range(self.quantidade_sistemas):
            equacao.append(self.equacao_protecao_inversor(sistema))
        
        return equacao

    def equacao_protecao_inversor(self,i):
        # equacao = fr"$I_{{\mathrm{{AG}}}} = \frac{{\mathrm{{potencia\ nominal }}}}{{\mathrm{{Tensao\ nominal * {self.multiplicador[i]}}}}} =\frac{{{self.potencia_inversores[i]}}}{{{self.inversor_tensao[i]* self.multiplicador[i]}}} = {self.corrente_saida_por_inversor[i]:.2f}\ A$" 
        equacao = (
            fr"$I_{{\mathrm{{AG}}}} = "
            fr"\frac{{\mathrm{{potencia\ nominal }}}}"
            fr"{{\mathrm{{Tensao\ nominal * {self.multiplicador[i]}}}}} = "
            fr"\frac{{{self.potencia_inversores[i]}}}"
            fr"{{{self.inversor_tensao[i] * self.multiplicador[i]}}} = "
            fr"{self.corrente_saida_por_inversor[i]:.2f}\ A$"
        )

        
        
        return equacao
    
    def equacao_queda_tensao(self):
        equacao4 = fr"$\Delta V \% = \frac{{200*\rho*L_c*I_c*cos\varphi}}{{S_c*V_f}}$"
        return equacao4

    def construtor_dados_memorial(self) -> RetornoProjetoCompleto:
        potencia_efetiva = round(self.calculo_potencia_efetiva(self.potencia_total_paineis_final), 2)
        
        return RetornoProjetoCompleto(logradouro_obra = self.projeto.endereco_obra['logradouro_obra'], 
            numero_obra = self.projeto.endereco_obra['numero_obra'],
            complemento_obra = self.projeto.endereco_obra['complemento_obra'],
            bairro_obra = self.projeto.endereco_obra['bairro_obra'],
            cidade_obra = self.projeto.endereco_obra['cidade_obra'],
            estado_obra = self.projeto.endereco_obra['estado_obra'],
            data_futura = ObjetosCalculados.data_futura(self.data_de_hoje()),
            cep_obra = self.projeto.endereco_obra['cep_obra'],
            latitude_obra = self.projeto.endereco_obra['latitude_obra'],
            longitude_obra = self.projeto.endereco_obra['longitude_obra'],

            nome_cliente = self.projeto.cliente['nome_cliente'],
            cpf = self.projeto.cliente['cpf'], 
            rg = self.projeto.cliente['rg'],
            razao_social = self.projeto.cliente['razao_social'],
            nome_fantasia = self.projeto.cliente['nome_fantasia'],
            cnpj = self.projeto.cliente['cnpj'],
            telefone = self.projeto.cliente['telefone_cliente'],
            email = self.projeto.cliente['email_cliente'],
            data_nascimento = self.projeto.cliente['data_nascimento'],
            data_hoje = ObjetosCalculados.data_de_hoje(self).strftime("%d de %B de %Y"),

            #dados elétricos do estabelecimento
            classe_consumo = self.projeto.classe_consumo1,
            carga_instalada_kw = self.projeto.carga_instalada_kw,
            energia_media_mensal_kwh = round(self.projeto.energia_media_mensal_kwh, 2),
            tensao_local = self.get_tensao_local(),
            tipo_fornecimento = self.projeto.tipo_fornecimento,
            disjuntor_geral = self.projeto.disjuntor_geral_amperes,
            
            #textos do memorial descritivo
            texto_placas_memorial = self.texto_placas_memorial, 
            texto_inversor_memorial = self.texto_inversor_memorial,
            texto_potencia_placa = self.texto_potencia_placa,
            texto_tensao_individual_paineis = self.texto_tensao_individual_paineis,
            texto_protecao_inversor = self.texto_protecao_inversor,
            texto_corrente_max_cabo = self.texto_corrente_max_cabo,
            texto_cabos = self.texto_cabos,
            texto_2_protecao_inversor = self.texto_2_protecao_inversor,
            gerador_texto_introducao = self.gerador_texto_introducao,
            gerador_texto_introducao2 = self.gerador_texto_introducao2,
            corrente_mp = self.corrente_maxima_potencia,
            corrente_cc = self.corrente_cc,
            tensao_circuito_aberto = self.texto_tensao_circuito_aberto,

            #dados painel
            tipo_celula = self.projeto.sistema_instalado[0].placa.tipo_celula,
            quantidade_final_placas = self.quantidade_final_placas,
            potencia_total_paineis_final = self.potencia_total_paineis_final,
            
            #dados inversor
            numero_total_strings = self.numero_total_strings,
            quantidade_final_de_placas_por_inversor = self.quantidade_final_de_placas_por_inversor,
            potencia_inversores = self.potencia_inversores,
            potencia_efetiva= potencia_efetiva,
            corrente_saida_por_inversor = self.corrente_saida_por_inversor,
            inversor_tensao = self.inversor_tensao,
            #calculos adicionais
            energia_gerada_mensal = round(self.energia_gerada(potencia_efetiva), 2),
            queda_tensao = self.tensao_queda,
            numero_uc = self.projeto.numero_unidade_consumidora,

            #equacoes
            equacao = self.equacao_demanda(),
            equacao2 = self.calculo_fator_de_carga(),
            equacao3 = self.conta_equacoes_inversor(),
            equacao4 = self.equacao_queda_tensao() )

