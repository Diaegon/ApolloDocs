# /home/d1aegon/Documentos/code/ApolloDocs/src/domain/creatememorialobject_v2.py
import locale
from datetime import datetime
from dateutil.relativedelta import relativedelta

from src.domain.utils.calculos import Calculos
from src.schemas.modelreturnobject import RetornoProjetoCompleto
from src.config import FORNECIMENTO_PARA_TENSAO, CLASSE_PARA_CODIGO

try:
    locale.setlocale(locale.LC_TIME, "pt_BR.utf8")
except locale.Error:
    locale.setlocale(locale.LC_TIME, "C")

class ObjetosCalculadosV2(Calculos):
    def __init__(self, projeto):
        self.projeto = projeto
        self.quantidade_sistemas = len(projeto.inversores) if projeto.inversores else 0
        self.numero_total_strings = 0
        self.multiplicador = []
        self.inversor_tensao = []
        self.quantidade_final_placas = 0
        self.potencia_total_paineis_final = 0
        self.quantidade_final_de_placas_por_inversor = []
        
        self.corrente_saida_por_inversor = []
        self.potencia_inversores = []
        self.tensao_queda = []
        self.cabos_energia_str = []
        self.disjuntores = []
        
        self.potencia_efetiva = 0.0
        self.energia_gerada_mensal = 0.0

    def calculate(self) -> "ObjetosCalculadosV2":
        self.checagem_inversores()
        self.calculo_disposicao_placas()
        
        self.potencia_efetiva = round(self.calculo_potencia_efetiva(self.potencia_total_paineis_final), 2)
        self.energia_gerada_mensal = round(self.energia_gerada(self.potencia_efetiva), 2)
        return self

    def get_multiplicador(self, numero_fases):
        if numero_fases == "monofasico":
            self.multiplicador.append(1)
            self.inversor_tensao.append(220)
        elif numero_fases == "trifasico":
            self.multiplicador.append(1.732)
            self.inversor_tensao.append(380)
        else:
            raise ValueError("Número de fases do inversor inválido")

    def checagem_inversores(self):
        for sistema in range(self.quantidade_sistemas):
            inversor = self.projeto.inversores[sistema].inversor
            
            self.get_multiplicador(inversor.numero_fases)
            
            corrente_saida = round(self.get_corrente_saida(
                inversor.potencia_inversor,
                self.multiplicador[sistema],
                self.inversor_tensao[sistema]
            ), 2)
            
            self.corrente_saida_por_inversor.append(corrente_saida)
            
            cabo = self.cabo_energia_inversor(corrente_saida)
            cabo_inteiro = int(cabo.split()[0])
            self.cabos_energia_str.append(cabo)
            
            self.potencia_inversores.append(inversor.potencia_inversor)
            
            queda = self.calculo_queda_tensao(
                int(corrente_saida),
                int(self.inversor_tensao[sistema]),
                cabo_inteiro
            )
            self.tensao_queda.append(queda)
            
            disjuntor = self.disjuntor_protecao(corrente_saida)
            self.disjuntores.append(disjuntor)

    def calculo_disposicao_placas(self):
        for placa_mat in self.projeto.placas:
            self.quantidade_final_placas += placa_mat.quantidade
            self.potencia_total_paineis_final += (placa_mat.quantidade * placa_mat.placa.potencia_placa) / 1000

        flat_inverters = []
        for inv_mat in self.projeto.inversores:
            for _ in range(inv_mat.quantidade):
                flat_inverters.append(inv_mat.inversor)

        num_inverters = len(flat_inverters)
        if num_inverters == 0:
            return

        sistemas = [{"inversor": inv, "placas_qty": 0} for inv in flat_inverters]
        for inv in flat_inverters:
            self.numero_total_strings += inv.numero_mppt

        total_placas = self.quantidade_final_placas
        base_qtd = total_placas // num_inverters
        remainder = total_placas % num_inverters

        for i in range(num_inverters):
            qtd = base_qtd + (1 if i < remainder else 0)
            sistemas[i]["placas_qty"] = qtd

        for sys in sistemas:
            numero_strings = sys["inversor"].numero_mppt
            placas = sys["placas_qty"]
            if numero_strings == 0:
                numero_strings = 1
                
            placas_por_string = placas // numero_strings
            resto_placas_por_string = placas % numero_strings
            
            lista_string = [placas_por_string] * numero_strings
            if resto_placas_por_string != 0:
                # DISTRIBUTE evenly +1 backwards (Best Practice)
                for idx in range(resto_placas_por_string):
                    lista_string[idx] += 1
            
            self.quantidade_final_de_placas_por_inversor.append(lista_string)

class MemorialPresenterV2:
    def __init__(self, projeto, calc: ObjetosCalculadosV2):
        self.projeto = projeto
        self.calc = calc

    def build(self) -> RetornoProjetoCompleto:
        return RetornoProjetoCompleto(
            **self._build_endereco(),
            **self._build_cliente(),
            **self._build_eletrico(),
            **self._build_textos_e_calculos(),
        )

    def _build_endereco(self) -> dict:
        hoje = datetime.now()
        data_futura = (hoje + relativedelta(months=1)).strftime("%d de %B de %Y")
        endereco = self.projeto.endereco_obra
        return {
            "logradouro_obra": getattr(endereco, "logradouro_obra", endereco.get("logradouro_obra", "") if isinstance(endereco, dict) else ""),
            "numero_obra": getattr(endereco, "numero_obra", endereco.get("numero_obra", "") if isinstance(endereco, dict) else ""),
            "complemento_obra": getattr(endereco, "complemento_obra", endereco.get("complemento_obra", "") if isinstance(endereco, dict) else ""),
            "bairro_obra": getattr(endereco, "bairro_obra", endereco.get("bairro_obra", "") if isinstance(endereco, dict) else ""),
            "cidade_obra": getattr(endereco, "cidade_obra", endereco.get("cidade_obra", "") if isinstance(endereco, dict) else ""),
            "estado_obra": getattr(endereco, "estado_obra", endereco.get("estado_obra", "") if isinstance(endereco, dict) else ""),
            "cep_obra": getattr(endereco, "cep_obra", endereco.get("cep_obra", "") if isinstance(endereco, dict) else ""),
            "latitude_obra": getattr(endereco, "latitude_obra", endereco.get("latitude_obra", "") if isinstance(endereco, dict) else 0),
            "longitude_obra": getattr(endereco, "longitude_obra", endereco.get("longitude_obra", "") if isinstance(endereco, dict) else 0),
            "data_hoje": hoje.strftime("%d de %B de %Y"),
            "data_futura": data_futura,
        }

    def _build_cliente(self) -> dict:
        c = self.projeto.cliente
        return {
            "nome_cliente": getattr(c, "nome_cliente", c.get("nome_cliente", "") if isinstance(c, dict) else ""),
            "cpf": getattr(c, "cpf", c.get("cpf", "") if isinstance(c, dict) else ""),
            "rg": getattr(c, "rg", c.get("rg", "") if isinstance(c, dict) else ""),
            "razao_social": getattr(c, "razao_social", c.get("razao_social", "") if isinstance(c, dict) else ""),
            "nome_fantasia": getattr(c, "nome_fantasia", c.get("nome_fantasia", "") if isinstance(c, dict) else ""),
            "cnpj": getattr(c, "cnpj", c.get("cnpj", "") if isinstance(c, dict) else ""),
            "telefone": getattr(c, "telefone_cliente", c.get("telefone_cliente", "") if isinstance(c, dict) else getattr(c, "telefone", "")),
            "email": getattr(c, "email_cliente", c.get("email_cliente", "") if isinstance(c, dict) else getattr(c, "email", "")),
            "data_nascimento": getattr(c, "data_nascimento", c.get("data_nascimento", "") if isinstance(c, dict) else ""),
        }

    def _build_eletrico(self) -> dict:
        p = self.projeto
        tensao_local = FORNECIMENTO_PARA_TENSAO.get(p.tipo_fornecimento, 220)
        classe_cliente = CLASSE_PARA_CODIGO.get(p.classe_consumo1, "B1")
        
        return {
            "classe_consumo": classe_cliente,
            "carga_instalada_kw": p.carga_instalada_kw,
            "energia_media_mensal_kwh": round(p.energia_media_mensal_kwh, 2),
            "tensao_local": tensao_local,
            "tipo_fornecimento": p.tipo_fornecimento,
            "disjuntor_geral": p.disjuntor_geral_amperes,
            "numero_uc": p.numero_unidade_consumidora,
        }

    def _build_textos_e_calculos(self) -> dict:
        list_placas = []
        tensao_max_pot = []
        pot_placa = []
        tensao_pico = []
        corrente_max_pot = []
        corrente_cc = []

        for index, placa_mat in enumerate(self.projeto.placas):
            p = placa_mat.placa
            qtd = placa_mat.quantidade
            sep = "  " if index == 0 else " "
            list_placas.append(f"{qtd}{sep}modulos {p.marca_placa} {p.modelo_placa}, de {p.potencia_placa}Wp")
            tensao_max_pot.append(str(p.tensao_maxima_potencia))
            pot_placa.append(str(p.potencia_placa))
            tensao_pico.append(str(p.tensao_pico))
            corrente_max_pot.append(str(p.corrente_maxima_potencia))
            corrente_cc.append(str(p.corrente_curtocircuito))

        list_inv = []
        list_prot = []
        list_corr_cabo = []
        marcas = []
        modelos = []
        
        for i in range(self.calc.quantidade_sistemas):
            inv_mat = self.projeto.inversores[i]
            inv = inv_mat.inversor
            qtd = inv_mat.quantidade
            disj = self.calc.disjuntores[i]
            corrente = self.calc.corrente_saida_por_inversor[i]
            
            list_inv.append(f"{qtd} inversor {inv.marca_inversor} {inv.modelo_inversor}")
            list_prot.append(f"{qtd} disjuntor de {disj} A")
            list_corr_cabo.append(self.calc.corrente_max_cabo(corrente))
            
            if inv.marca_inversor not in marcas:
                marcas.append(inv.marca_inversor)
            modelos.append(inv.modelo_inversor)

        resultado_D = self.projeto.energia_media_mensal_kwh / 720
        eq_D = rf"$D_{{\mathrm{{media}}}} = \frac{{\mathrm{{Energia\ media}}}}{{N^{{\circ}}\,\mathrm{{de\ horas}}}} = \frac{{{self.projeto.energia_media_mensal_kwh}}}{{720}} = {resultado_D:.2f}\ kW$"
        
        fc = resultado_D / self.projeto.carga_instalada_kw
        eq_FC = rf"$FC = \frac{{\mathrm{{Energia}}}}{{\mathrm{{Potencia \ instalada \ x \ 720h}}}} = \frac{{{self.projeto.energia_media_mensal_kwh}}}{{{self.projeto.carga_instalada_kw} \ x  \ 720}} = {fc:.2f}\ kW$"

        eq3_list = []
        for i in range(self.calc.quantidade_sistemas):
            p = self.calc.potencia_inversores[i]
            v = self.calc.inversor_tensao[i]
            m = self.calc.multiplicador[i]
            c = self.calc.corrente_saida_por_inversor[i]
            eq3_list.append(rf"$I_{{\mathrm{{AG}}}} = \frac{{\mathrm{{potencia\ nominal }}}}{{\mathrm{{Tensao\ nominal * {m}}}}} = \frac{{{p}}}{{{v * m}}} = {c:.2f}\ A$")

        eq4 = r"$\Delta V \% = \frac{200*\rho*L_c*I_c*cos\varphi}{S_c*V_f}$"

        return {
            "texto_placas_memorial": ", ".join(list_placas),
            "texto_inversor_memorial": ", ".join(list_inv),
            "texto_potencia_placa": ", ".join(pot_placa),
            "texto_tensao_individual_paineis": ", ".join(tensao_max_pot),
            "texto_protecao_inversor": ", ".join(list_prot),
            "texto_corrente_max_cabo": ", ".join(list_corr_cabo),
            "texto_cabos": self.calc.cabos_energia_str,
            "texto_2_protecao_inversor": self.calc.disjuntores,
            "gerador_texto_introducao": ", ".join(marcas),
            "gerador_texto_introducao2": " ".join(modelos),
            "corrente_mp": ", ".join(corrente_max_pot),
            "corrente_cc": ", ".join(corrente_cc),
            "tensao_circuito_aberto": ", ".join(tensao_pico),
            "tipo_celula": self.projeto.placas[0].placa.tipo_celula if len(self.projeto.placas) > 0 else "Monocristalino",
            "quantidade_final_placas": self.calc.quantidade_final_placas,
            "potencia_total_paineis_final": self.calc.potencia_total_paineis_final,
            "numero_total_strings": self.calc.numero_total_strings,
            "quantidade_final_de_placas_por_inversor": self.calc.quantidade_final_de_placas_por_inversor,
            "potencia_inversores": self.calc.potencia_inversores,
            "potencia_efetiva": self.calc.potencia_efetiva,
            "corrente_saida_por_inversor": self.calc.corrente_saida_por_inversor,
            "inversor_tensao": self.calc.inversor_tensao,
            "energia_gerada_mensal": self.calc.energia_gerada_mensal,
            "queda_tensao": self.calc.tensao_queda,
            "equacao": eq_D,
            "equacao2": eq_FC,
            "equacao3": eq3_list,
            "equacao4": eq4,
        }
