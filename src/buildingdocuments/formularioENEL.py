from io import BytesIO
import fitz

from api.schemas.projetos.formularioenelce import ProjetoFormularioEnelCe

from src.config import (
    FORMULARIO_ENELCEARA_MENOR_OU_IGUAL_10K,
    FORMULARIO_ENELCEARA_MAIOR_10K,
)

from src.schemas.constantes import (
    POTENCIA_MAXIMA_MONOFASICA,
    TENSAO_MONOFASICA,
    TENSAO_TRIFASICA,
    CLASSECONSUMO_RESIDENCIAL,
    CLASSECONSUMO_COMERCIAL,
    CLASSECONSUMO_RURAL,
)


class FormularioEnelCe:
    def __init__(self, dados_projeto: ProjetoFormularioEnelCe):
        self.dados_projeto = dados_projeto
        self.buffer = BytesIO()
        self.escolhe_pdf()

    def escolhe_pdf(self):
        if self.dados_projeto.potencia_geracao <= POTENCIA_MAXIMA_MONOFASICA:
            self.pdf_base = FORMULARIO_ENELCEARA_MENOR_OU_IGUAL_10K
        else:
            self.pdf_base = FORMULARIO_ENELCEARA_MAIOR_10K

    def check_tensaolocal(self):
        tensao_local = self.dados_projeto.tensao_local
        if tensao_local == TENSAO_MONOFASICA:
            return "Monofásica"
        elif tensao_local == TENSAO_TRIFASICA:
            return "Trifásica"

    def check_classe(self):
        classe_consumo = self.dados_projeto.classe
        if classe_consumo == "residencial":
            return CLASSECONSUMO_RESIDENCIAL
        elif classe_consumo == "comercial":
            return CLASSECONSUMO_COMERCIAL
        elif classe_consumo == "rural":
            return CLASSECONSUMO_RURAL

    def inserir_dados_form(self, page):
        def preencher_por_frase(page, item, valor):
            palavra = page.search_for(item)
            rect = palavra[0]

            x = rect.x1 + 6
            y = rect.y1

            page.insert_text((x, y), valor, fontsize=9, fontname="helv")

        def preencher_solicitante(page, item, valor):
            palavra = page.search_for(item)
            rect = palavra[2]

            x = rect.x1 + 6
            y = rect.y1

            page.insert_text((x, y), valor, fontsize=9, fontname="helv")

        def preencher_assinatura(page, item, valor):
            palavra = page.search_for(item)
            rect = palavra[0]

            x = rect.x0 - 10
            y = rect.y0 - 4

            page.insert_text((x, y), valor, fontsize=9, fontname="helv")

        def preencher_caixas_padrao(page, item, valor):
            palavra = page.search_for(item)
            rect = palavra[0]
            x = rect.x0 - 10
            y = rect.y1

            page.insert_text((x, y), valor, fontsize=9, fontname="helv")

        def preencher_caixa_tensao(
            page, item=self.check_tensaolocal(), valor="X"
        ):
            palavra = page.search_for(item)
            rect = palavra[0]
            x = rect.x0 - 10
            y = rect.y1

            page.insert_text((x, y), valor, fontsize=9, fontname="helv")

        CAMPOS_UC = {
            "Código da UC:": f"{self.dados_projeto.numero_uc}",
            "Titular da UC :": f"{self.dados_projeto.nome_cliente}",
            "Rua/Av.:": f"{self.dados_projeto.endereco_obra.logradouro_obra}",
            "Nº:": f"{self.dados_projeto.endereco_obra.numero_obra}",
            "CEP:": f"{self.dados_projeto.endereco_obra.cep_obra}",
            "Bairro:": f"{self.dados_projeto.endereco_obra.bairro_obra}",
            "Cidade:": f"{self.dados_projeto.endereco_obra.cidade_obra}",
            "E-mail:": f"{self.dados_projeto.email_cliente}",
            "Telefone:": f"{self.dados_projeto.telefone_cliente}",
            "CNPJ/CPF:": f"{self.dados_projeto.cpf}",
            "Latitude:": f"{self.dados_projeto.endereco_obra.latitude_obra}",
            "Longitude:": f"{self.dados_projeto.endereco_obra.longitude_obra}",
            "Potência instalada (kW):": f"{self.dados_projeto.carga_instalada_kw}",
            "Tensão de atendimento (V):": f"{self.dados_projeto.tensao_local}",
            "Potência instalada de geração (kW):": f"{self.dados_projeto.potencia_geracao}",
            "Classe": f"{self.check_classe()}  {self.dados_projeto.classe.value}",
            "Nome/Procurador Legal:": f"{self.dados_projeto.nome_procurador}",
        }

        CAMPOS_SOLICITANTE = {
            "Telefone:": "TESTE",
            "E-mail:": "TESTE",
        }

        CAMPOS_ASSINATURA = {
            "Local": "TESTE",
            "Data": "TESTE",
        }

        CAIXAS = {
            "Grupo B": "X",
            "Solar": "X",
        }

        for item, valor in CAMPOS_UC.items():
            preencher_por_frase(page, item, valor)

        for item, valor in CAMPOS_SOLICITANTE.items():
            preencher_solicitante(page, item, valor)

        for item, valor in CAMPOS_ASSINATURA.items():
            preencher_assinatura(page, item, valor)

        for item, valor in CAIXAS.items():
            preencher_caixas_padrao(page, item, valor)

        preencher_caixa_tensao(page)

    def to_bytes(self):
        return self.buffer.getvalue()

    def gerar_formulario(self) -> BytesIO:  # noqa: PLR0915
        doc = fitz.open(self.pdf_base)
        page = doc[0]
        self.inserir_dados_form(page)
        doc.save(self.buffer)
        doc.close()
        self.buffer.seek(0)

        return self.buffer
