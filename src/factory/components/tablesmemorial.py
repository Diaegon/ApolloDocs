import json
from reportlab.platypus import Table, Paragraph, TableStyle
from src.schemas.tableschemas import styles, estilotabela, estilotabelaloc, estilo_tabela_parametros, estilo_assinatura

class TablesBuilder():
    def __init__(self,retorno):
        self.retorno = retorno

    def tabeladedados(self):
        dados = [[f"UC: {self.retorno.numero_uc}"], 
         [f"CLASSE: {self.retorno.classe_consumo} {self.retorno.tipo_fornecimento}"], 
         [f"Nome do Cliente: {self.retorno.nome_cliente}"],
         [f"Endereço: {self.retorno.logradouro_obra}, {self.retorno.numero_obra}  {self.retorno.complemento_obra}, {self.retorno.bairro_obra},{self.retorno.cidade_obra} {self.retorno.estado_obra}."],
         [f"CEP:{self.retorno.cep_obra}"],
         [f"CPF/CNPJ: {self.retorno.cpf}"]]
        
        tabeladedados = Table(dados)
        tabeladedados.setStyle(estilotabela)

        return tabeladedados#tabela localização da obra

    def tabela_localizacao(self):
        loc_instalacao = [["COORDENADAS - coordenadas decimais - WGS 84 "],
                  [" Local de implantação do Gerador fotovoltaico",
                      "Lat: ", "Long: "],
                  ["", f"{self.retorno.latitude_obra}", f"{self.retorno.longitude_obra}"]]

        tabela_localizacao = Table(loc_instalacao)
        tabela_localizacao.setStyle(estilotabelaloc)
        return tabela_localizacao


    def tabelapainel(self):
        #tabelas especificações técnicas
        modulo_caracteristicas = [["Potência nominal máx. (Pmax) ", f"({self.retorno.texto_potencia_placa} )Wp"],
                                ["Tensão operacional opt. (Vmp) ", f"({self.retorno.texto_tensao_individual_paineis} )V"],
                                ["Corrente operacional opt. (Imp)", f"({self.retorno.corrente_mp}) A"], 
                                ["Tensão circuito aberto (Voc) ", f"({self.retorno.tensao_circuito_aberto} )V"], 
                                ["Corrente curto-circuito (Isc)", f"({self.retorno.corrente_cc}) A"]]
        tabelapainel = Table(modulo_caracteristicas)
        tabelapainel.setStyle(estilotabela)
        return tabelapainel

    def tabela_parametros_tensao_inversor(self):
        #tabela parametrização inversor
        parametros_tensao_inversor = [["Faixa de tensão no ponto de conexão [V]","Tempo de desconexão [s]"],
                                    ["TL > 231","0,2 s"], 
                                    ["189 ≤ TL ≤ 231","Operação Normal"], 
                                    ["TL < 195,5","0,2 s"]]
        tabela_parametros_tensao_inversor = Table(parametros_tensao_inversor)
        tabela_parametros_tensao_inversor.setStyle(estilo_tabela_parametros)
        return tabela_parametros_tensao_inversor
    
    def tabela_parametros_frequencia_inversor(self):
        parametros_frequencia_inversor = [["Faixa de freqüência no ponto de conexão (Hz)","Tempo de desconexão [s]"],
                                        ["f ≤ 57,5","0,2"],
                                        ["59,9 < f ≤ 60,1","Operação normal"],
                                        ["f > 62,5","0,2"] ]
        tabela_parametros_frequencia_inversor = Table(parametros_frequencia_inversor)
        tabela_parametros_frequencia_inversor.setStyle(estilo_tabela_parametros)
        return tabela_parametros_frequencia_inversor
    
    def tabela_parametros_fp_inversor(self):        
        parametros_fp_inversor = [["Potência Nominal (W) - Pn","Faixa de fator de potência","Fator de potência \nconfiguração em fábrica"],
                                [f"{self.retorno.potencia_inversores}","0,95 indutivo – 0,95 capacitivo","1"]]
        tabela_parametros_fp_inversor = Table(parametros_fp_inversor)
        tabela_parametros_fp_inversor.setStyle(estilo_tabela_parametros)
        return tabela_parametros_fp_inversor

    def tabela_queda_tensao(self):
        #parametros de queda de tensão
        queda_tensao = [["ρ  - resistividade do cobre","0,0173"],
                        [Paragraph("L<sub>c</sub> - comprimento do condutor",styles["CorpoTexto"]),"10 m"], 
                        [Paragraph("I<sub>c</sub> - corrente do condutor",styles["CorpoTexto"]),f"{self.retorno.corrente_saida_por_inversor} A"],
                        ["Cosφ - fator de potencia","1"],
                        [Paragraph("S<sub>c</sub> - Seção reta do condutor",styles["CorpoTexto"]), f"{self.retorno.texto_cabos}mm²"], 
                        [Paragraph("V <sub>f</sub> - tensão ", styles["CorpoTexto"]), f"{self.retorno.inversor_tensao} v"]]
        tabela_queda_tensao = Table(queda_tensao)
        tabela_queda_tensao.setStyle(estilotabela)
        return tabela_queda_tensao

    def tabela_assinatura(self, cliente_nome, cliente_cpf, data):
        #assinatura do cliente.
        assinatura = [[""],[f"                  {cliente_nome}, CPF:{cliente_cpf}                    "], [f"{data}"]]
        tabela_assinatura = Table(assinatura)
        tabela_assinatura.setStyle(estilo_assinatura)
        return tabela_assinatura

