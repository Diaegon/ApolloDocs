from io import BytesIO
import fitz

from api.schemas.projetos.formularioenelce import ProjetoFormularioEnelCe

from src.config import (
    FORMULARIO_ENELCEARA_MENOR_OU_IGUAL_10K,
    FORMULARIO_ENELCEARA_MAIOR_10K
)

from src.schemas.constantes import (
    POTENCIA_MAXIMA_MONOFASICA,
    TENSAO_MONOFASICA,
    TENSAO_TRIFASICA,
    CLASSECONSUMO_RESIDENCIAL,
    CLASSECONSUMO_COMERCIAL,
    CLASSECONSUMO_RURAL
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

    def preencher_formulario(self, page):
        if self.dados_projeto.potencia_geracao <= POTENCIA_MAXIMA_MONOFASICA:
            self.inserir_dados_no_formulario(page)
        else:
            self.inserir_dados_no_formulario_10k(page)

    def check_tensaolocal(self):
        tensao_local = self.dados_projeto.tensao_local
        if tensao_local == TENSAO_MONOFASICA:
            return "monofasico"
        elif tensao_local == TENSAO_TRIFASICA:
            return "trifasico"
    def check_classe(self):
        classe_consumo = self.dados_projeto.classe
        if classe_consumo == "residencial":
            return CLASSECONSUMO_RESIDENCIAL
        elif classe_consumo == "comercial":
            return CLASSECONSUMO_COMERCIAL
        elif classe_consumo == "rural":
            return CLASSECONSUMO_RURAL    
    def inserir_dados_no_formulario_10k(self, page):
        # dados cliente
        # primeira linha
        page.insert_text(
            (45, 100),
            f"{self.dados_projeto.numero_uc}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (165, 100), "X", fontsize=9, fontname="helv", color=(0, 0, 0)
        )
        page.insert_text(
            (360, 100),
            f"{self.check_classe()}",
            fontsize=8,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (410, 100),
            f"{self.dados_projeto.classe} {self.check_tensaolocal()}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        # segunda linha
        page.insert_text(
            (45, 110),
            f"{self.dados_projeto.nome_cliente}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        # terceira linha
        page.insert_text(
            (45, 118),
            f"{self.dados_projeto.endereco_obra.logradouro_obra}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (270, 118),
            f"{self.dados_projeto.endereco_obra.numero_obra} {self.dados_projeto.endereco_obra.complemento_obra}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (370, 118),
            f"{self.dados_projeto.endereco_obra.cep_obra} ",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        # quarta linha
        page.insert_text(
            (45, 128),
            f"{self.dados_projeto.endereco_obra.bairro_obra}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (185, 128),
            f"{self.dados_projeto.endereco_obra.cidade_obra}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (45, 138),
            f"{self.dados_projeto.email_cliente}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (45, 147),
            f"{self.dados_projeto.telefone_cliente}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (45, 156),
            f"{self.dados_projeto.cpf}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )

        # dados unidade consumidora
        # primeira linha
        page.insert_text(
            (190, 183),
            f"{self.dados_projeto.endereco_obra.latitude_obra}",
            fontsize=6,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (300, 183),
            f"{self.dados_projeto.endereco_obra.longitude_obra}",
            fontsize=6,
            fontname="helv",
            color=(0, 0, 0),
        )
        # segunda linha
        page.insert_text(
            (70, 192),
            f"{self.dados_projeto.carga_instalada_kw}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (340, 192),
            f"{self.dados_projeto.tensao_local} V",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        # terceira linha
        page.insert_text(
            (360, 202), "X", fontsize=7, fontname="helv", color=(0, 0, 0)
        )
        # quarta linha
        if self.dados_projeto.ramal_energia == "aereo":
            page.insert_text(
                (165, 220), "X", fontsize=7, fontname="helv", color=(0, 0, 0)
            )
        else:
            page.insert_text(
                (265, 220), "X", fontsize=7, fontname="helv", color=(0, 0, 0)
            )
        # Dados da geração
        # primeira linha
        page.insert_text(
            (100, 246),
            f"{self.dados_projeto.potencia_geracao}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )

        # Dados procurador
        # primeira linha
        page.insert_text(
            (70, 455),
            f"{self.dados_projeto.nome_procurador}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (30, 465),
            f"{self.dados_projeto.telefone_procurador}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (30, 475),
            f"{self.dados_projeto.email_procurador}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (20, 492),
            "Fortaleza",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (99, 492),
            f"{self.dados_projeto.data_hoje}",
            fontsize=12,
            fontname="helv",
            color=(0, 0, 0),
        )
    def inserir_dados_no_formulario(self, page):

        # dados cliente
        # primeira linha
        page.insert_text(
            (47, 119),
            f"{self.dados_projeto.numero_uc}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (195, 119), "X", fontsize=9, fontname="helv", color=(0, 0, 0)
        )
        page.insert_text(
            (430, 119),
            f"{self.check_classe()}",
            fontsize=8,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (480, 119),
            f"{self.dados_projeto.classe} {self.check_tensaolocal()}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        # segunda linha
        page.insert_text(
            (47, 134),
            f"{self.dados_projeto.nome_cliente}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        # terceira linha
        page.insert_text(
            (47, 148),
            f"{self.dados_projeto.endereco_obra.logradouro_obra}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (318, 148),
            f"{self.dados_projeto.endereco_obra.numero_obra} {self.dados_projeto.endereco_obra.complemento_obra}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (430, 148),
            f"{self.dados_projeto.endereco_obra.cep_obra} ",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        # quarta linha
        page.insert_text(
            (47, 160),
            f"{self.dados_projeto.endereco_obra.bairro_obra}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (220, 160),
            f"{self.dados_projeto.endereco_obra.cidade_obra}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (47, 174),
            f"{self.dados_projeto.email_cliente}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (47, 186),
            f"{self.dados_projeto.telefone_cliente}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (47, 200),
            f"{self.dados_projeto.cpf}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )

        # dados unidade consumidora
        # primeira linha
        page.insert_text(
            (221, 230),
            f"{self.dados_projeto.endereco_obra.latitude_obra}",
            fontsize=6,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (351, 230),
            f"{self.dados_projeto.endereco_obra.longitude_obra}",
            fontsize=6,
            fontname="helv",
            color=(0, 0, 0),
        )
        # segunda linha
        page.insert_text(
            (75, 243),
            f"{self.dados_projeto.carga_instalada_kw}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (390, 243),
            f"{self.dados_projeto.tensao_local} V",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        # terceira linha
        if self.check_tensaolocal() == "monofasico":
            page.insert_text(
                (195, 257), "X", fontsize=7, fontname="helv", color=(0, 0, 0)
            )
        else:
            page.insert_text(
                (420, 257), "X", fontsize=7, fontname="helv", color=(0, 0, 0)
            )

        # quarta linha
        if self.dados_projeto.ramal_energia == "aereo":
            page.insert_text(
                (195, 285), "X", fontsize=7, fontname="helv", color=(0, 0, 0)
            )
        else:
            page.insert_text(
                (310, 285), "X", fontsize=7, fontname="helv", color=(0, 0, 0)
            )
        # Dados da geração
        # primeira linha

        page.insert_text(
            (107, 317),
            f"{self.dados_projeto.potencia_geracao}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )

        page.insert_text(
            (510, 345), "X", fontsize=7, fontname="helv", color=(0, 0, 0)
        )
        # Dados procurador
        # primeira linha
        page.insert_text(
            (75, 665),
            f"{self.dados_projeto.nome_procurador}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (35, 680),
            f"{self.dados_projeto.telefone_procurador}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (30, 695),
            f"{self.dados_projeto.email_procurador}",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (20, 720),
            "Fortaleza",
            fontsize=7,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (102, 720),
            f"{self.dados_projeto.data_hoje}",
            fontsize=12,
            fontname="helv",
            color=(0, 0, 0),
        )

    def to_bytes(self):
        return self.buffer.getvalue()
    
    def gerar_formulario(self) -> BytesIO:  # noqa: PLR0915
        doc = fitz.open(self.pdf_base)
        page = doc[0]
        self.preencher_formulario(page)
        doc.save(self.buffer)
        doc.close()
        self.buffer.seek(0)

        return self.buffer