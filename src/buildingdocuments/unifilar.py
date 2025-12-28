from io import BytesIO

import fitz

from src.config import (
    DIAGRAMA_UNIFILAR_TEMPLATE_1,
    DIAGRAMA_UNIFILAR_TEMPLATE_2,
    DIAGRAMA_UNIFILAR_TEMPLATE_3,
)
from src.schemas.modelreturnobject import RetornoProjetoDiagrama


class DiagramaUnifilar:
    def __init__(self, dados_projeto: RetornoProjetoDiagrama):
        self.dados_projeto = dados_projeto
        self.buffer = BytesIO()
        self.pdf_base = self.escolha_template()

    def escolha_template(self):
        UM_SISTEMA = 1
        DOIS_SISTEMAS = 2
        TRES_SISTEMAS = 3

        if self.dados_projeto.quantidade_sistemas_instalados == UM_SISTEMA:
            return DIAGRAMA_UNIFILAR_TEMPLATE_1
        elif (
            self.dados_projeto.quantidade_sistemas_instalados == DOIS_SISTEMAS
        ):
            return DIAGRAMA_UNIFILAR_TEMPLATE_2
        elif (
            self.dados_projeto.quantidade_sistemas_instalados == TRES_SISTEMAS
        ):
            return DIAGRAMA_UNIFILAR_TEMPLATE_3
        else:
            raise ValueError("Quantidade inválida")

    def desenhar_diagrama(self, page):
        DOIS_SISTEMAS = 2
        TRES_SISTEMAS = 3
        self.funcao_lado_do_inversor(page)
        if self.dados_projeto.quantidade_sistemas_instalados >= DOIS_SISTEMAS:
            self.funcao_lado_do_inversor2(page)
        if self.dados_projeto.quantidade_sistemas_instalados >= TRES_SISTEMAS:
            self.funcao_lado_do_inversor3(page)

        self.funcao_lado_rede(page)
        self.funcao_dados_gerais(page)

    def gerar_diagrama(self) -> BytesIO:
        doc = fitz.open(self.pdf_base)
        page = doc[0]  # primeira página

        self.desenhar_diagrama(page)

        doc.save(self.buffer)
        doc.close()

        self.buffer.seek(0)  # MUITO IMPORTANTE
        return self.buffer

    def funcao_dados_gerais(self, page):
        # dados {proprietario}
        page.insert_text(
            (1245, 920),
            f"{self.dados_projeto.nome_cliente}",
            fontsize=5,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (1245, 1035),
            f"{self.dados_projeto.endereco_obra.logradouro_obra},"
            f"{self.dados_projeto.endereco_obra.numero_obra}, "
            f"{self.dados_projeto.endereco_obra.complemento_obra},"
            f"{self.dados_projeto.endereco_obra.bairro_obra},"
            f"{self.dados_projeto.endereco_obra.cidade_obra}.",
            fontsize=5,
            fontname="helv",
            color=(0, 0, 0),
        )
        # DADOS PROJETISTA
        page.insert_text(
            (1245, 785),
            f"ELETROTÉCNICO: {self.dados_projeto.nome_projetista}",
            fontsize=5,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (1245, 790),
            f"CFT: {self.dados_projeto.cft_crea_projetista}",
            fontsize=5,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (1245, 937),
            f"{self.dados_projeto.nome_cliente}",
            fontsize=5,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (1335, 937),
            f"{self.dados_projeto.data_hoje}",
            fontsize=5,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (1375, 937),
            f"{self.dados_projeto.endereco_obra.cidade_obra}",
            fontsize=5,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (1315, 230),
            f"{self.dados_projeto.potencia_total_placas / 1000} kWp / {self.dados_projeto.potencia_total_inversores / 1000} kW",
            fontsize=12,
            fontname="helv",
            color=(0, 0, 0),
        )

    def funcao_lado_rede(self, page):
        MONOFASICO = 220
        TRIFASICO = 380

        if self.dados_projeto.tensao_local == MONOFASICO:
            page.insert_text(
                (860, 555),
                f"{self.dados_projeto.texto_disjuntorgeral_unifilar}",
                fontsize=6,
                fontname="helv",
                color=(0, 0, 0),
            )
            page.insert_text(
                (925, 555),
                "MEDIDOR\nMONOFÁSICO",
                fontsize=6,
                fontname="helv",
                color=(0, 0, 0),
            )
        elif self.dados_projeto.tensao_local == TRIFASICO:
            page.insert_text(
                (860, 555),
                f"{self.dados_projeto.texto_disjuntorgeral_unifilar}",
                fontsize=6,
                fontname="helv",
                color=(0, 0, 0),
            )
            page.insert_text(
                (925, 555),
                "MEDIDOR\nTRIFÁSICO",
                fontsize=6,
                fontname="helv",
                color=(0, 0, 0),
            )
            # linhas do disjuntor
            page.draw_line(
                p1=(880, 530), p2=(880, 537), color=(0, 0, 0), width=0.5
            )
            page.draw_line(
                p1=(886, 530), p2=(886, 537), color=(0, 0, 0), width=0.5
            )
            # LINHAS DO CABO
            page.draw_line(
                p1=(773, 536), p2=(773, 547), color=(0, 0, 0), width=0.5
            )
            page.draw_line(
                p1=(770, 536), p2=(770, 547), color=(0, 0, 0), width=0.5
            )

    def funcao_lado_do_inversor(self, page):
        page.insert_text(
            (370, 570),
            f"{self.dados_projeto.texto_paineis1}",
            fontsize=12,
            fontname="helv",
            color=(0, 0, 0),
        )
        # texto inversores
        page.insert_text(
            (553, 503),
            f"{self.dados_projeto.texto_inversor1}",
            fontsize=8,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (643, 507),
            f"{self.dados_projeto.cabo_inversor1} mm²",
            fontsize=8,
            fontname="helv",
            color=(0, 0, 0),
        )
        if (
            self.dados_projeto.sistema_instalado1.inversor.numero_fases
            == "monofasico"
        ):
            page.insert_text(
                (680, 555),
                f"{self.dados_projeto.texto_disjuntor_protecao1}",
                fontsize=6,
                fontname="helv",
                color=(0, 0, 0),
            )
        elif (
            self.dados_projeto.sistema_instalado1.inversor.numero_fases
            == "trifasico"
        ):
            page.insert_text(
                (680, 555),
                f"{self.dados_projeto.texto_disjuntor_protecao1}",
                fontsize=6,
                fontname="helv",
                color=(0, 0, 0),
            )
            # linhas do cabo
            page.draw_line(
                p1=(652, 534), p2=(652, 545), color=(0, 0, 0), width=0.5
            )
            page.draw_line(
                p1=(648, 534), p2=(648, 545), color=(0, 0, 0), width=0.5
            )
            # linhas do disjuntor
            page.draw_line(
                p1=(696, 530), p2=(696, 536), color=(0, 0, 0), width=0.5
            )
            page.draw_line(
                p1=(700, 530), p2=(700, 536), color=(0, 0, 0), width=0.5
            )

    def funcao_lado_do_inversor2(self, page):
        page.insert_text(
            (370, 450),
            f"{self.dados_projeto.texto_paineis2}",
            fontsize=12,
            fontname="helv",
            color=(0, 0, 0),
        )
        # texto inversores
        page.insert_text(
            (528, 383),
            f"{self.dados_projeto.texto_inversor2}",
            fontsize=8,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (618, 387),
            f"{self.dados_projeto.cabo_inversor2} mm²",
            fontsize=8,
            fontname="helv",
            color=(0, 0, 0),
        )
        if (
            self.dados_projeto.sistema_instalado2.inversor.numero_fases
            == "monofasico"
        ):
            page.insert_text(
                (660, 435),
                f"{self.dados_projeto.texto_disjuntor_protecao2}",
                fontsize=6,
                fontname="helv",
                color=(0, 0, 0),
            )
        elif (
            self.dados_projeto.sistema_instalado2.inversor.numero_fases
            == "trifasico"
        ):
            page.insert_text(
                (660, 435),
                f"{self.dados_projeto.texto_disjuntor_protecao2}",
                fontsize=6,
                fontname="helv",
                color=(0, 0, 0),
            )
            # linhas do cabo
            page.draw_line(
                p1=(626, 416), p2=(626, 427), color=(0, 0, 0), width=0.5
            )
            page.draw_line(
                p1=(621, 416), p2=(621, 427), color=(0, 0, 0), width=0.5
            )
            # linhas do disjuntor
            page.draw_line(
                p1=(671, 412), p2=(671, 419), color=(0, 0, 0), width=0.5
            )
            page.draw_line(
                p1=(676, 412), p2=(676, 419), color=(0, 0, 0), width=0.5
            )

    def funcao_lado_do_inversor3(self, page):
        page.insert_text(
            (370, 330),
            f"{self.dados_projeto.texto_paineis3}",
            fontsize=12,
            fontname="helv",
            color=(0, 0, 0),
        )
        # texto inversores
        page.insert_text(
            (528, 263),
            f"{self.dados_projeto.texto_inversor3}",
            fontsize=8,
            fontname="helv",
            color=(0, 0, 0),
        )
        page.insert_text(
            (618, 267),
            f"{self.dados_projeto.cabo_inversor3} mm²",
            fontsize=8,
            fontname="helv",
            color=(0, 0, 0),
        )
        if (
            self.dados_projeto.sistema_instalado3.inversor.numero_fases
            == "monofasico"
        ):
            page.insert_text(
                (660, 315),
                f"{self.dados_projeto.texto_disjuntor_protecao3}",
                fontsize=6,
                fontname="helv",
                color=(0, 0, 0),
            )
        elif (
            self.dados_projeto.sistema_instalado3.inversor.numero_fases
            == "trifasico"
        ):
            page.insert_text(
                (660, 315),
                f"{self.dados_projeto.texto_disjuntor_protecao3}",
                fontsize=6,
                fontname="helv",
                color=(0, 0, 0),
            )
            # linhas do cabo
            page.draw_line(
                p1=(626, 298), p2=(626, 309), color=(0, 0, 0), width=0.5
            )
            page.draw_line(
                p1=(621, 298), p2=(621, 309), color=(0, 0, 0), width=0.5
            )
            # linhas do disjuntor
            page.draw_line(
                p1=(671, 294), p2=(671, 301), color=(0, 0, 0), width=0.5
            )
            page.draw_line(
                p1=(676, 294), p2=(676, 301), color=(0, 0, 0), width=0.5
            )

    def to_bytes(self):
        return self.buffer.getvalue()
