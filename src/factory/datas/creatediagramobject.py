from src.schemas.modelreturnobject import RetornoProjetoDiagrama
from src.schemas.schemas import ProjetoUnifilar
from src.factory.datas.utils.calculos import Calculos
from datetime import date

class ObjetoDiagramaUnifilar:
    def __init__(self, dados_projeto: ProjetoUnifilar):
        self.dados_projeto = dados_projeto
        self.checagem_sistemas()
        self.potencia_total_inversores = 0
        self.potencia_total_placas = 0
    
    def checagem_sistemas(self):
        self.quantidade_sistemas = self.dados_projeto.quantidade_sistemas_instalados
        

    def texto_disjuntorgeral_unifilar(self):
        if self.dados_projeto.tensao_local == 220:
            return f"DISJUNTOR\nMONOFÁSICO\n \n{self.dados_projeto.disjuntor_geral_amperes} A - 220V"
        elif self.dados_projeto.tensao_local == 380:
            return f"DISJUNTOR\nTRIFÁSICO\n \n{self.dados_projeto.disjuntor_geral_amperes} A - 380/220V"
    
    def get_multiplicador(self, tensao_inversor: str):
        if tensao_inversor == "monofasico":
            return 1
        elif tensao_inversor == "trifasico":
            return 1.73

    def get_tensao(self, tensao_inversor: str):
        if tensao_inversor == "monofasico":
            return 220
        elif tensao_inversor == "trifasico":
            return 380
        
    def texto_disjuntor_protecao1(self, sistema_instalado):
        sistema1 = sistema_instalado
        tensao_inversor = sistema1.inversor.numero_fases
        multiplicador = self.get_multiplicador(tensao_inversor)
        tensao = self.get_tensao(tensao_inversor)
        corrente_saida_inversor = Calculos.get_corrente_saida(
            potencia_inversor=sistema1.inversor.potencia_inversor * 1000 * sistema1.quantidade_inversor,
            multiplicador=multiplicador,
            inversor_tensao=tensao
        )
        
        disjuntor_protecao1 = Calculos.disjuntor_protecao(corrente_saida_inversor)
        if tensao_inversor == "monofasico":
            return f"DISJUNTOR\nMONOFÁSICO\n{disjuntor_protecao1} A - 220V"
        elif tensao_inversor == "trifasico":
            return f"DISJUNTOR\nTRIFÁSICO\n{disjuntor_protecao1} A - 380V"
    
    def cabo_inversor1(self, sistema_instalado):
        sistema1 = sistema_instalado
        tensao_inversor = sistema1.inversor.numero_fases
        multiplicador = self.get_multiplicador(tensao_inversor)
        tensao = self.get_tensao(tensao_inversor)
        corrente_saida_inversor = Calculos.get_corrente_saida(
            potencia_inversor=sistema1.inversor.potencia_inversor * 1000 * sistema1.quantidade_inversor,
            multiplicador=multiplicador,
            inversor_tensao=tensao    
        )
        cabo_inversor1 = Calculos.cabo_energia_inversor(corrente_saida_inversor)
        return cabo_inversor1

    def texto_paineis(self, sistema_instalado):
        sistema = sistema_instalado
        if not sistema.quantidade_total_placas_do_sistema.quantidade_placas2:
            quantidade_placa = sistema.quantidade_total_placas_do_sistema.quantidade_placas
            marca_placa = sistema.placa.marca_placa
            modelo_placa = sistema.placa.modelo_placa
            self.potencia_total_placas += sistema.placa.potencia_placa * quantidade_placa
            return f"{quantidade_placa}x " + f" {marca_placa} \n {modelo_placa}"
        
        else:
            quantidade_placa1 = sistema.quantidade_total_placas_do_sistema.quantidade_placas
            quantidade_placa2 = sistema.quantidade_total_placas_do_sistema.quantidade_placas2
            self.potencia_total_placas += sistema.placa.potencia_placa * quantidade_placa1
            self.potencia_total_placas += sistema.placa2.potencia_placa * quantidade_placa2

            marca_placa = sistema.placa.marca_placa
            marca_placa2 = sistema.placa2.marca_placa
            modelo_placa = sistema.placa.modelo_placa
            modelo_placa2 = sistema.placa2.modelo_placa

            return f"{quantidade_placa1}x " + f" {marca_placa} \n {modelo_placa} + \n" + f"{quantidade_placa2}x " + f" {marca_placa2} \n {modelo_placa2}"

    def texto_inversor1(self, sistema_instalado):
        sistema1 = sistema_instalado
        marca_inversor = sistema1.inversor.marca_inversor
        modelo_inversor = sistema1.inversor.modelo_inversor
        potencia_inversor = sistema1.inversor.potencia_inversor
        quantidade_inversor = sistema1.quantidade_inversor
        self.potencia_total_inversores += potencia_inversor * quantidade_inversor
        return f"{quantidade_inversor}x {marca_inversor} \n {modelo_inversor} - {potencia_inversor} kW"

    def construir_dados_diagrama(self) -> RetornoProjetoDiagrama:
        if self.quantidade_sistemas == 2:
            texto_disjuntor_protecao2 = self.texto_disjuntor_protecao1(self.dados_projeto.sistema_instalado2)
            texto_paineis2 = self.texto_paineis(self.dados_projeto.sistema_instalado2)
            cabo_inversor2 = self.cabo_inversor1(self.dados_projeto.sistema_instalado2)
            sistema_instalado2 = self.dados_projeto.sistema_instalado2
            texto_inversor2 = self.texto_inversor1(self.dados_projeto.sistema_instalado2)
            texto_disjuntor_protecao3 = None
            texto_paineis3 = None
            cabo_inversor3 = None
            texto_inversor3 = None
            sistema_instalado3 = None
        elif self.quantidade_sistemas == 3:
            texto_disjuntor_protecao2 = self.texto_disjuntor_protecao1(self.dados_projeto.sistema_instalado2)
            texto_disjuntor_protecao3 = self.texto_disjuntor_protecao1(self.dados_projeto.sistema_instalado3)
            texto_paineis2 = self.texto_paineis(self.dados_projeto.sistema_instalado2)
            texto_paineis3 = self.texto_paineis(self.dados_projeto.sistema_instalado3)
            cabo_inversor2 = self.cabo_inversor1(self.dados_projeto.sistema_instalado2)
            cabo_inversor3 = self.cabo_inversor1(self.dados_projeto.sistema_instalado3)
            sistema_instalado2 = self.dados_projeto.sistema_instalado2
            sistema_instalado3 = self.dados_projeto.sistema_instalado3
            texto_inversor2 = self.texto_inversor1(self.dados_projeto.sistema_instalado2)
            texto_inversor3 = self.texto_inversor1(self.dados_projeto.sistema_instalado3)
        
        else:
            texto_disjuntor_protecao2 = None
            texto_disjuntor_protecao3 = None
            texto_paineis2 = None
            texto_paineis3 = None
            cabo_inversor2 = None
            cabo_inversor3 = None
            texto_inversor2 = None
            texto_inversor3 = None
            sistema_instalado2 = None
            sistema_instalado3 = None

        return RetornoProjetoDiagrama(
            quantidade_sistemas_instalados=self.quantidade_sistemas,
          
            sistema_instalado1=self.dados_projeto.sistema_instalado1,

            sistema_instalado2 = sistema_instalado2,

            sistema_instalado3 = sistema_instalado3,

            nome_cliente=self.dados_projeto.nome_cliente,
            
            endereco_obra=self.dados_projeto.endereco_obra,

            texto_disjuntorgeral_unifilar= self.texto_disjuntorgeral_unifilar(),
            
            texto_disjuntor_protecao1= self.texto_disjuntor_protecao1(self.dados_projeto.sistema_instalado1),

            texto_disjuntor_protecao2= texto_disjuntor_protecao2,

            texto_disjuntor_protecao3= texto_disjuntor_protecao3,

            texto_paineis1 = self.texto_paineis(self.dados_projeto.sistema_instalado1),

            texto_paineis2 = texto_paineis2,
            
            texto_paineis3 = texto_paineis3,

            cabo_inversor1 = self.cabo_inversor1(self.dados_projeto.sistema_instalado1),

            cabo_inversor2 = cabo_inversor2,

            cabo_inversor3 = cabo_inversor3,

            nome_projetista = self.dados_projeto.nome_projetista,

            cft_crea_projetista = self.dados_projeto.cft_crea_projetista,

            texto_inversor1 = self.texto_inversor1(self.dados_projeto.sistema_instalado1),

            texto_inversor2 = texto_inversor2,

            texto_inversor3 = texto_inversor3,
                       
            tensao_local = self.dados_projeto.tensao_local,
            
            data_hoje = date.today().strftime("%d/%m/%Y"),

            potencia_total_inversores = self.potencia_total_inversores,

            potencia_total_placas = self.potencia_total_placas
        )