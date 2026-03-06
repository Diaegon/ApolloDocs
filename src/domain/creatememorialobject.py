# por enquanto objeto está aqui, mas o ideal é isntanciar de outro lugar
import locale
from datetime import datetime

from dateutil.relativedelta import relativedelta

from src.domain.utils.calculos import Calculos
from src.schemas.modelreturnobject import (
    RetornoProjetoCompleto,
)

try:
    locale.setlocale(locale.LC_TIME, "pt_BR.utf8")
except locale.Error:
    # fallback seguro para servidores como o Render
    locale.setlocale(locale.LC_TIME, "C")


class ObjetosCalculados(Calculos):
    def __init__(self, projeto):
        self.projeto = projeto
        self.numero_total_strings = 0
        self.quantidade_sistemas = 0
        self.multiplicador = []
        self.inversor_tensao = []
        self.quantidade_final_placas = 0
        self.potencia_total_paineis_final = 0
        self.quantidade_final_de_placas_por_inversor = []
        # text fields — built as lists and joined in construtor_dados_memorial
        self._list_placas_memorial = []
        self._list_inversor_memorial = []
        self._list_potencia_placa = []
        self._list_tensao_individual_paineis = []
        self._list_tensao_circuito_aberto = []
        self._list_corrente_maxima_potencia = []
        self._list_corrente_cc = []
        self._list_protecao_inversor = []
        self._list_corrente_max_cabo = []
        self.texto_cabos = []
        self.texto_2_protecao_inversor = []
        self.potencia_inversores = []
        self.potencia_total_inversores_final = 0
        self.tensao_queda = []
        self.corrente_saida_por_inversor = []
        self._list_introducao2 = []
        self.lista_equacoes_protecao_inversores = []

    def calculate(self) -> "ObjetosCalculados":
        """Run all engineering calculations and populate internal state.

        Separated from __init__ so that:
        - The object can be inspected / partially configured before computing.
        - Individual steps can be mocked in unit tests.
        - The caller is explicit about when computation happens.

        Returns self to allow fluent chaining:
            retorno = ObjetosCalculados(projeto).calculate().construtor_dados_memorial()
        """
        self.checagem_sistemas_instalados()
        self.checagem_inversores()
        self.checagem_placas()
        self.calculo_disposicao_placas()
        return self

    def checagem_sistemas_instalados(self):
        sistemas_instalados = self.projeto.sistema_instalado
        self.quantidade_sistemas = len(sistemas_instalados)

    def get_multiplicador(self, sistema, numero_fases) -> float:
        """Retorna o multiplicador baseado no número de fases."""
        numero_fases = self.projeto.sistema_instalado[
            sistema
        ].inversor.numero_fases
        if numero_fases == "monofasico":
            self.multiplicador.append(1)
            self.inversor_tensao.append(220)
        elif numero_fases == "trifasico":
            self.multiplicador.append(1.732)
            self.inversor_tensao.append(380)
        else:
            raise ValueError("Número de fases do inversor inválido")

    def get_classe_codigo(self):
        """Retorna o código de classe da ANEEL para o tipo de consumo."""
        CLASSE_PARA_CODIGO = {
            "residencial": "B1",
            "rural": "B2",
            "comercial": "B3",
        }
        classe_cliente = self.projeto.classe_consumo
        if classe_cliente not in CLASSE_PARA_CODIGO:
            raise ValueError(
                f"Classe de consumo inválida: '{classe_cliente}'. "
                f"Valores aceitos: {list(CLASSE_PARA_CODIGO)}"
            )
        return CLASSE_PARA_CODIGO[classe_cliente]

    def get_tensao_local(self) -> int:
        """Retorna a tensão local em volts com base no tipo de fornecimento."""
        FORNECIMENTO_PARA_TENSAO = {
            "monofasico": 220,
            "bifasico": 220,
            "trifasico": 380,
        }
        tensao_cliente = self.projeto.tipo_fornecimento
        if tensao_cliente not in FORNECIMENTO_PARA_TENSAO:
            raise ValueError(
                f"Tipo de fornecimento inválido: '{tensao_cliente}'. "
                f"Valores aceitos: {list(FORNECIMENTO_PARA_TENSAO)}"
            )
        return FORNECIMENTO_PARA_TENSAO[tensao_cliente]

    def checagem_inversores(self):
        marca_de_inversores = []
        modelo_inversores = []

        for sistema in range(self.quantidade_sistemas):
            quantidade_inversor = self.projeto.sistema_instalado[
                sistema
            ].quantidade_inversor
            marca_de_inversores.append(
                self.projeto.sistema_instalado[sistema].inversor.marca_inversor
            )
            modelo_inversores = self.projeto.sistema_instalado[
                sistema
            ].inversor.modelo_inversor
            potencia_inversor = self.projeto.sistema_instalado[
                sistema
            ].inversor.potencia_inversor
            numero_fases = self.projeto.sistema_instalado[
                sistema
            ].inversor.numero_fases

            self.get_multiplicador(sistema, numero_fases)
            corrente_saida_inversor = round(
                self.get_corrente_saida(
                    potencia_inversor,
                    self.multiplicador[sistema],
                    self.inversor_tensao[sistema],
                ),
                2,
            )
            self.corrente_saida_por_inversor.append(corrente_saida_inversor)
            cabo = self.cabo_energia_inversor(corrente_saida_inversor)
            cabo_inteiro = int(cabo.split()[0])

            self.potencia_inversores.append(potencia_inversor)
            queda_tensao = self.calculo_queda_tensao(
                int(corrente_saida_inversor),
                int(self.inversor_tensao[sistema]),
                cabo_inteiro,
            )
            self.tensao_queda.append(queda_tensao)
            disjuntor_protecao = self.disjuntor_protecao(
                corrente_saida_inversor
            )

            self.texto_cabos.append(cabo)
            self.texto_2_protecao_inversor.append(disjuntor_protecao)
            self._list_protecao_inversor.append(
                f"{quantidade_inversor} disjuntor de {disjuntor_protecao} A"
            )
            self._list_corrente_max_cabo.append(
                self.corrente_max_cabo(corrente_saida_inversor)
            )
            self._list_inversor_memorial.append(
                f"{quantidade_inversor} inversor {marca_de_inversores[-1]} {modelo_inversores}"
            )
            self._list_introducao2.append(modelo_inversores)

        # deduplicate brands for the introduction sentence
        seen = set()
        unique_marcas = []
        for marca in marca_de_inversores:
            if marca not in seen:
                seen.add(marca)
                unique_marcas.append(marca)
        self.gerador_texto_introducao = ", ".join(unique_marcas)

    def _monta_texto_placa_individual(self, item, placa_attr, qtd_index):
        """Shared helper used for both placa and placa2 to avoid duplication."""
        sistemas_instalados = self.projeto.sistema_instalado[item]
        qtd_lista = list(
            sistemas_instalados.quantidade_total_placas_do_sistema.model_dump().values()
        )
        placa = getattr(sistemas_instalados, placa_attr)
        quantidade = qtd_lista[qtd_index]

        self._list_tensao_individual_paineis.append(str(placa.tensao_maxima_potencia))
        self._list_potencia_placa.append(str(placa.potencia_placa))
        self._list_tensao_circuito_aberto.append(str(placa.tensao_pico))
        self._list_corrente_maxima_potencia.append(str(placa.corrente_maxima_potencia))
        self._list_corrente_cc.append(str(placa.corrente_curtocircuito))

        sep = "  " if qtd_index == 0 else " "
        return f"{quantidade}{sep}modulos {placa.marca_placa} {placa.modelo_placa}, de {placa.potencia_placa}Wp"

    def checagem_placas(self):
        for item in range(self.quantidade_sistemas):
            sistemas_instalados = self.projeto.sistema_instalado[item]
            quantidade_placas_lista = list(
                sistemas_instalados.quantidade_total_placas_do_sistema.model_dump().values()
            )

            self._list_placas_memorial.append(
                self._monta_texto_placa_individual(item, "placa", 0)
            )
            if quantidade_placas_lista[1]:
                self._list_placas_memorial.append(
                    self._monta_texto_placa_individual(item, "placa2", 1)
                )

    # conta a quantidade de placas de um sistema considerando que um sistema só vai ter no máximo dois tipos de placa.
    def conta_placa_do_sistema(self, i):
        sistemas_instalados = self.projeto.sistema_instalado[i]
        quantidade_final = []
        # debug
        quantidade_placas_lista = list(
            sistemas_instalados.quantidade_total_placas_do_sistema.model_dump().values()
        )

        quantidade_placa1 = quantidade_placas_lista[0]
        modelo = sistemas_instalados.placa.modelo_placa
        marca = sistemas_instalados.placa.marca_placa
        potencia = sistemas_instalados.placa.potencia_placa
        quantidade_ = [modelo, marca, potencia, quantidade_placa1]
        quantidade_final.append(quantidade_)
        self.quantidade_final_placas += quantidade_placa1

        # monta a lista
        #
        if quantidade_placas_lista[1] not in {None, 0}:
            quantidade_placa2 = quantidade_placas_lista[1]
            modelo2 = sistemas_instalados.placa2.modelo_placa
            marca2 = sistemas_instalados.placa2.marca_placa
            potencia2 = sistemas_instalados.placa2.potencia_placa
            quantidade_2 = [modelo2, marca2, potencia2, quantidade_placa2]
            quantidade_final.append(quantidade_2)
            self.quantidade_final_placas += quantidade_placa2

        return quantidade_final

    # calcula a distribuição das placas no inversor, como nesse self.projeto cada sistema só tem um inversor, fica mais simples o calculo
    # vamos deixar a resposta crua sem identificar quais placas vão ser arranjadas;
    def distribui_placa_por_inversor(self, quantidade_sistemas):
        numero_strings = self.projeto.sistema_instalado[
            quantidade_sistemas
        ].inversor.numero_mppt
        self.numero_total_strings += numero_strings
        placas_sistema = self.conta_placa_do_sistema(quantidade_sistemas)
        numero_painel1 = placas_sistema[0][3]
        self.potencia_total_paineis_final += (
            placas_sistema[0][3] * placas_sistema[0][2]
        ) / 1000
        numero_de_paineis = numero_painel1
        if len(placas_sistema) > 1 and placas_sistema[1][3] not in {None, 0}:
            numero_painel2 = placas_sistema[1][3]
            self.potencia_total_paineis_final += (
                placas_sistema[1][3] * placas_sistema[1][2]
            ) / 1000
            numero_de_paineis += numero_painel2

        lista_string = []

        resto_placas_por_string = numero_de_paineis % numero_strings
        placas_por_string = numero_de_paineis // numero_strings
        for numero_mppt in range(numero_strings):
            lista_string.append(placas_por_string)
        if resto_placas_por_string != 0:
            lista_string[-1] += resto_placas_por_string
        return lista_string

    # aqui iteramos sobre cada sistema instalado
    def calculo_disposicao_placas(self):
        for quantidade_sistemas in range(
            self.projeto.quantidade_sistemas_instalados
        ):
            quantidade_de_placas_por_inversor = (
                self.distribui_placa_por_inversor(quantidade_sistemas)
            )
            self.quantidade_final_de_placas_por_inversor.append(
                quantidade_de_placas_por_inversor
            )
        # retornamos a quantidade final de placas caso tenha mais de um sistema instalado.

    @staticmethod
    def data_de_hoje():
        data_de_hoje = datetime.now()
        # data_futura = data_de_hoje+relativedelta(months=1)
        # locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
        # plt.rcParams['text.usetex'] = True # Ativar o uso do LaTeX real (MikTeX)
        return data_de_hoje

    def data_futura(data_de_hoje):
        data_futura = data_de_hoje + relativedelta(months=1)
        data_futura = data_futura.strftime("%d de %B de %Y")
        return data_futura

    def equacao_demanda(self):
        resultado = self.projeto.energia_media_mensal_kwh / 720
        equacao = rf"$D_{{\mathrm{{media}}}} = \frac{{\mathrm{{Energia\ media}}}}{{N^{{\circ}}\,\mathrm{{de\ horas}}}} = \frac{{{self.projeto.energia_media_mensal_kwh}}}{{720}} = {resultado:.2f}\ kW$"
        return equacao

    def calculo_fator_de_carga(self):
        fatordecarga = (
            self.projeto.energia_media_mensal_kwh / 720
        ) / self.projeto.carga_instalada_kw
        equacao2 = rf"$FC = \frac{{\mathrm{{Energia}}}}{{\mathrm{{Potencia \ instalada \ x \ 720h}}}} = \frac{{{self.projeto.energia_media_mensal_kwh}}}{{{self.projeto.carga_instalada_kw} \ x  \ 720}} = {fatordecarga:.2f}\ kW$"
        return equacao2

    def conta_equacoes_inversor(self):
        equacao = []
        for sistema in range(self.quantidade_sistemas):
            equacao.append(self.equacao_protecao_inversor(sistema))

        return equacao

    def equacao_protecao_inversor(self, i):
        # equacao = fr"$I_{{\mathrm{{AG}}}} = \frac{{\mathrm{{potencia\ nominal }}}}{{\mathrm{{Tensao\ nominal * {self.multiplicador[i]}}}}} =\frac{{{self.potencia_inversores[i]}}}{{{self.inversor_tensao[i]* self.multiplicador[i]}}} = {self.corrente_saida_por_inversor[i]:.2f}\ A$"
        equacao = (
            rf"$I_{{\mathrm{{AG}}}} = "
            rf"\frac{{\mathrm{{potencia\ nominal }}}}"
            rf"{{\mathrm{{Tensao\ nominal * {self.multiplicador[i]}}}}} = "
            rf"\frac{{{self.potencia_inversores[i]}}}"
            rf"{{{self.inversor_tensao[i] * self.multiplicador[i]}}} = "
            rf"{self.corrente_saida_por_inversor[i]:.2f}\ A$"
        )

        return equacao

    @staticmethod
    def equacao_queda_tensao():
        equacao4 = (
            r"$\Delta V \% = \frac{200*\rho*L_c*I_c*cos\varphi}{S_c*V_f}$"
        )
        return equacao4

    # -----------------------------------------------------------------------
    # Private builders — each assembles one logical group of DTO fields
    # -----------------------------------------------------------------------

    def _build_endereco(self) -> dict:
        """Location and date fields for the work address."""
        hoje = ObjetosCalculados.data_de_hoje()
        endereco = self.projeto.endereco_obra
        return {
            "logradouro_obra": endereco["logradouro_obra"],
            "numero_obra": endereco["numero_obra"],
            "complemento_obra": endereco.get("complemento_obra", ""),
            "bairro_obra": endereco["bairro_obra"],
            "cidade_obra": endereco["cidade_obra"],
            "estado_obra": endereco["estado_obra"],
            "cep_obra": endereco["cep_obra"],
            "latitude_obra": endereco.get("latitude_obra", ""),
            "longitude_obra": endereco.get("longitude_obra", ""),
            "data_hoje": hoje.strftime("%d de %B de %Y"),
            "data_futura": ObjetosCalculados.data_futura(hoje),
        }

    def _build_cliente(self) -> dict:
        """Client identification fields. Optional fields default to empty string."""
        c = self.projeto.cliente
        return {
            "nome_cliente": c["nome_cliente"],
            "cpf": c["cpf"],
            "rg": c["rg"],
            "razao_social": c.get("razao_social", ""),
            "nome_fantasia": c.get("nome_fantasia", ""),
            "cnpj": c.get("cnpj", ""),
            "telefone": c["telefone_cliente"],
            "email": c["email_cliente"],
            "data_nascimento": c["data_nascimento"],
        }

    def _build_eletrico(self) -> dict:
        """Electrical characteristics of the consumption unit."""
        p = self.projeto
        return {
            "classe_consumo": p.classe_consumo1,
            "carga_instalada_kw": p.carga_instalada_kw,
            "energia_media_mensal_kwh": round(p.energia_media_mensal_kwh, 2),
            "tensao_local": self.get_tensao_local(),
            "tipo_fornecimento": p.tipo_fornecimento,
            "disjuntor_geral": p.disjuntor_geral_amperes,
            "numero_uc": p.numero_unidade_consumidora,
        }

    def _build_textos_e_calculos(self, potencia_efetiva: float) -> dict:
        """Composed text strings, panel/inverter data, and derived calculations."""
        return {
            # --- Composed text strings (joined, no trailing commas) ---
            "texto_placas_memorial": ", ".join(self._list_placas_memorial),
            "texto_inversor_memorial": ", ".join(self._list_inversor_memorial),
            "texto_potencia_placa": ", ".join(self._list_potencia_placa),
            "texto_tensao_individual_paineis": ", ".join(self._list_tensao_individual_paineis),
            "texto_protecao_inversor": ", ".join(self._list_protecao_inversor),
            "texto_corrente_max_cabo": ", ".join(self._list_corrente_max_cabo),
            "texto_cabos": self.texto_cabos,
            "texto_2_protecao_inversor": self.texto_2_protecao_inversor,
            "gerador_texto_introducao": self.gerador_texto_introducao,
            "gerador_texto_introducao2": " ".join(self._list_introducao2),
            "corrente_mp": ", ".join(self._list_corrente_maxima_potencia),
            "corrente_cc": ", ".join(self._list_corrente_cc),
            "tensao_circuito_aberto": ", ".join(self._list_tensao_circuito_aberto),
            # --- Panel data ---
            "tipo_celula": self.projeto.sistema_instalado[0].placa.tipo_celula,
            "quantidade_final_placas": self.quantidade_final_placas,
            "potencia_total_paineis_final": self.potencia_total_paineis_final,
            # --- Inverter data ---
            "numero_total_strings": self.numero_total_strings,
            "quantidade_final_de_placas_por_inversor": self.quantidade_final_de_placas_por_inversor,
            "potencia_inversores": self.potencia_inversores,
            "potencia_efetiva": potencia_efetiva,
            "corrente_saida_por_inversor": self.corrente_saida_por_inversor,
            "inversor_tensao": self.inversor_tensao,
            # --- Derived calculations ---
            "energia_gerada_mensal": round(self.energia_gerada(potencia_efetiva), 2),
            "queda_tensao": self.tensao_queda,
            # --- Equations ---
            "equacao": self.equacao_demanda(),
            "equacao2": self.calculo_fator_de_carga(),
            "equacao3": self.conta_equacoes_inversor(),
            "equacao4": self.equacao_queda_tensao(),
        }

    # -----------------------------------------------------------------------
    # Public constructor — orchestrates builders into the final DTO
    # -----------------------------------------------------------------------

    def construtor_dados_memorial(self) -> RetornoProjetoCompleto:
        potencia_efetiva = round(
            self.calculo_potencia_efetiva(self.potencia_total_paineis_final), 2
        )
        return RetornoProjetoCompleto(
            **self._build_endereco(),
            **self._build_cliente(),
            **self._build_eletrico(),
            **self._build_textos_e_calculos(potencia_efetiva),
        )
