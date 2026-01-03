from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

from src.domain.components.imagesmemorial import InsertImage
from src.domain.components.tablesmemorial import TablesBuilder
from src.domain.texts.text_memorial import TextoMemorial
from src.schemas.tableschemas import styles


class MemorialDescritivo:
    def __init__(self, dados):
        self.dados = dados
        self.texto = TextoMemorial(dados)
        self.tabela = TablesBuilder(dados)
        self.imagens = InsertImage()
        self.buffer = BytesIO()
        self.doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            leftMargin=2 * cm,
            rightMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
        )

    def gerar_memorial(self):  # noqa: PLR0915
        story = []
        # CAPA @@ NÃO MUDA NADA
        story.append(Paragraph("MEMORIAL DESCRITIVO", styles["Title"]))
        story.append(Spacer(1, 2 * cm))
        story.append(
            Paragraph("PROJETO DE GERAÇÃO DISTRIBUÍDA", styles["Heading1"])
        )
        story.append(Spacer(1, 3 * cm))
        story.append(
            Paragraph(
                f" PROJETO PARA IMPLANTAÇÃO DE GERADOR FOTOVOLTAICO NA ÁREA {self.dados.classe_consumo} DO(A) Cliente: {self.dados.nome_cliente}",
                styles["Heading3"],
            )
        )
        story.append(
            Paragraph(f"Local: {self.dados.cidade_obra}", styles["Heading3"])
        )
        story.append(Paragraph(self.texto.texto_data(), styles["Heading4"]))
        story.append(PageBreak())

        # SUMARIO @@NÂO MUDA NADA

        story.append(Paragraph("SUMÁRIO", styles["TituloSecao"]))
        story.append(Spacer(1, 2 * cm))
        topicos = [
            ("1 - INTRODUÇÃO", 3),
            ("1.1 - Identificação do cliente", 3),
            ("2 - LOCALIZAÇÃO DO GERADOR FOTOVOLTAICO", 3),
            ("2.1 - Planta de situação do gerador", 3),
            ("3 -CARGA INSTALADA ", 4),
            ("3.1 - Cálculo da Demanda Média", 4),
            ("3.2 - Cálculo do Fator de Carga Médio", 4),
            ("4 - GERADOR FOTOVOLTAICO", 4),
            ("4.1 - Cálculo da Energia Média Gerad5", 5),
            ("5 - DIAGRAMAS BÁSICOS", 5),
            ("5.1 - Parametrização do inverso", 5),
            ("5.1.x - tabelas de parametrização do inversor", 6),
            ("6 - INSTALAÇÃO ELÉTRICA", 6),
            ("6.1 – Diagrama unifilar Geral", 6),
            ("6.2 – Dimensionamento da Proteção", 6),
            ("6.3 – Coordenação entre os Disjuntores", 7),
            ("7 – SINALIZAÇÃO", 8),
            ("8 – RESPONSÁVEL TÉCNICO", 9),
        ]
        for titulo, pagina in topicos:
            linha = self.linha_sumario(titulo, pagina)
            story.append(Paragraph(linha, styles["SubSecao"]))

        story.append(PageBreak())
        # DOC
        story.append(Paragraph("1 - INTRODUÇÃO", styles["TituloSecao"]))
        story.append(Spacer(1, 1 * cm))

        # primeiro texto - introdução
        story.append(
            Paragraph(self.texto.texto_introducao(), styles["CorpoTexto"])
        )
        story.append(Spacer(1, 1 * cm))

        # ###IDENTIFICAÇÃO DO CLIENTE
        story.append(
            Paragraph("1.1 - Identificação do cliente", styles["SubSecao"])
        )
        story.append(self.tabela.tabeladedados())
        story.append(Spacer(1, 2 * cm))

        # ## segundo texto - localização
        story.append(
            Paragraph(
                "2 - LOCALIZAÇÃO DO GERADOR FOTOVOLTAICO",
                styles["TituloSecao"],
            )
        )
        story.append(Spacer(1, 1 * cm))
        story.append(
            Paragraph("2.1 -Planta de situação do gerador", styles["SubSecao"])
        )
        story.append(Paragraph(self.texto.texto_loc(), styles["CorpoTexto"]))
        story.append(self.tabela.tabela_localizacao())
        story.append(Spacer(1, 0.5 * cm))
        story.append(Paragraph(self.texto.texto_loc2(), styles["CorpoTexto"]))
        story.append(PageBreak())

        # ## terceiro texto - carga instalada
        story.append(Paragraph("3 - CARGA INSTALADA", styles["TituloSecao"]))
        story.append(Spacer(1, 1 * cm))
        story.append(
            Paragraph(self.texto.texto_carginst(), styles["CorpoTexto"])
        )
        story.append(Spacer(1, 1 * cm))
        story.append(
            Paragraph("3.1 - Cálculo da Demanda Média", styles["SubSecao"])
        )
        story.append(
            Paragraph(self.texto.texto_calculo_demanda(), styles["CorpoTexto"])
        )
        self.imagens.insert_equation(self.dados.equacao, story)

        story.append(
            Paragraph(
                self.texto.texto_calculo_demanda2(), styles["CorpoTexto"]
            )
        )
        story.append(Spacer(1, 1 * cm))
        story.append(
            Paragraph(
                "3.2 - Cálculo do Fator de Carga Médio", styles["SubSecao"]
            )
        )
        story.append(
            Paragraph(self.texto.texto_calculo_fc(), styles["CorpoTexto"])
        )

        self.imagens.insert_equation(self.dados.equacao2, story)

        story.append(Spacer(1, 1 * cm))
        story.append(
            Paragraph("4 - GERADOR FOTOVOLTAICO", styles["TituloSecao"])
        )
        story.append(Spacer(1, 1 * cm))
        story.append(
            Paragraph(self.texto.texto_geradorfv(), styles["CorpoTexto"])
        )
        story.append(self.tabela.tabelapainel())
        story.append(
            Paragraph(self.texto.texto_potenciafv(), styles["CorpoTexto"])
        )
        story.append(Spacer(1, 1 * cm))
        story.append(
            Paragraph(
                "4.1 - Cálculo da Energia Média Gerada ", styles["SubSecao"]
            )
        )
        story.append(
            Paragraph(
                self.texto.texto_calculo_enegiagerada(), styles["CorpoTexto"]
            )
        )
        story.append(Spacer(1, 2 * cm))
        story.append(Paragraph("5 - DIAGRAMAS BÁSICOS", styles["TituloSecao"]))
        story.append(Spacer(1, 1 * cm))
        story.append(
            Paragraph(self.texto.texto_diagramas(), styles["CorpoTexto"])
        )
        story.append(self.imagens.imagem_diagrama())
        story.append(Spacer(1, 1 * cm))
        story.append(
            Paragraph("5.1 - Parametrização do inversor ", styles["SubSecao"])
        )
        story.append(Spacer(1, 1 * cm))
        story.append(
            Paragraph(self.texto.texto_parametrizacao(), styles["CorpoTexto"])
        )
        story.append(Spacer(1, 2 * cm))
        story.append(
            Paragraph(
                "5.1.1 - Ajuste de sobre e Subtensão ", styles["SubSecao"]
            )
        )
        story.append(self.tabela.tabela_parametros_tensao_inversor())
        story.append(Spacer(1, 1 * cm))
        story.append(
            Paragraph(
                "5.1.2 - Ajustes dos Limites de Freqüência (sobre e subfreqüência) ",
                styles["SubSecao"],
            )
        )
        story.append(self.tabela.tabela_parametros_frequencia_inversor())
        story.append(Spacer(1, 1 * cm))
        story.append(
            Paragraph(
                " 5.1.3 - Ajustes do Limite do Fator de Potência",
                styles["SubSecao"],
            )
        )
        story.append(self.tabela.tabela_parametros_fp_inversor())
        story.append(Spacer(1, 2 * cm))
        story.append(
            Paragraph("6 - INSTALAÇÃO ELÉTRICA", styles["TituloSecao"])
        )
        story.append(
            Paragraph(self.texto.texto_instalacao(), styles["CorpoTexto"])
        )
        story.append(Spacer(1, 1 * cm))
        story.append(
            Paragraph(" 6.1 – Diagrama unifilar Geral", styles["SubSecao"])
        )
        story.append(
            Paragraph(self.texto.texto_diagramauni(), styles["CorpoTexto"])
        )
        story.append(Spacer(1, 1 * cm))
        story.append(
            Paragraph(
                " 6.2 – Dimensionamento da Proteção e Alimentação do Gerador Fotovoltaico",
                styles["SubSecao"],
            )
        )
        story.append(
            Paragraph(
                self.texto.texto_dimensionamento_protecao(),
                styles["CorpoTexto"],
            )
        )
        story.append(PageBreak())

        self.imagens.insert_equation_current(self.dados.equacao3, story)

        # AJEITAR ESSA LÓGICA PARA NÃO PRECISAR DO IF NO MEIO DO GERADOR DE TEXTO.

        story.append(Spacer(1, 1 * cm))
        story.append(
            Paragraph(
                self.texto.texto_dimensionamento_protecao2(),
                styles["CorpoTexto"],
            )
        )

        self.imagens.insert_equation(self.dados.equacao4, story)

        story.append(Spacer(1, 1 * cm))
        story.append(self.tabela.tabela_queda_tensao())
        story.append(Spacer(1, 1 * cm))
        story.append(
            Paragraph(
                self.texto.texto_dimensionamento_protecao3(),
                styles["CorpoTexto"],
            )
        )
        story.append(
            Paragraph(
                " 6.3 – Coordenação entre o Disjuntor do Gerador Fotovoltaico e da Proteção Geral",
                styles["SubSecao"],
            )
        )
        story.append(Spacer(1, 1 * cm))
        story.append(
            Paragraph(self.texto.texto_disjuntores(), styles["CorpoTexto"])
        )
        story.append(PageBreak())
        story.append(Paragraph("7 – SINALIZAÇÃO", styles["TituloSecao"]))
        story.append(
            Paragraph(self.texto.texto_sinalizacao(), styles["CorpoTexto"])
        )

        story.append(self.imagens.imagem_aviso())

        story.append(Spacer(1, 2 * cm))
        story.append(PageBreak())
        story.append(
            Paragraph("8 – RESPONSÁVEL TÉCNICO", styles["TituloSecao"])
        )
        story.append(Spacer(1, 3 * cm))

        story.append(self.imagens.imagem_assinatura())

        self.doc.build(
            story,
            onFirstPage=self.add_page_number,
            onLaterPages=self.add_page_number,
        )

    def to_bytes(self):
        return self.buffer.getvalue()

    @staticmethod
    def linha_sumario(titulo, pagina, largura_pontilhado=80):
        """Retorna uma string formatada com pontilhado entre título e página"""
        max_linha = largura_pontilhado
        texto_base = f"{titulo} "
        dots = "." * max(3, max_linha - len(texto_base) - len(str(pagina)))
        return f"{texto_base}{dots} {pagina}"

    @staticmethod
    def add_page_number(canvas, doc):
        page_num = canvas.getPageNumber()
        text = f"Página {page_num}"
        canvas.setFont("Helvetica", 9)
        width, height = doc.pagesize
        canvas.drawCentredString(width / 2.0, 1.5 * cm, text)
