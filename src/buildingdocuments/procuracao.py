from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from src.schemas.tableschemas import styles
from src.factory.texts.text_procuracao import TextoProcuracao
from src.factory.components.tablesmemorial import TablesBuilder
from io import BytesIO
from datetime import datetime

class Procuracao:
    def __init__(self, projeto):
        self.projeto = projeto
        self.buffer = BytesIO()
        self.texto = TextoProcuracao(projeto)
        self.tabela = TablesBuilder(projeto)
        self.data = datetime.now().strftime("%d/%m/%Y")
        self.doc = SimpleDocTemplate(self.buffer, 
                                    pagesize=A4, 
                                    leftMargin=2*cm, rightMargin=2*cm,
                                    topMargin=2*cm, bottomMargin=2*cm) 
    def gerar_procuracao(self):
        procuracao = []
        procuracao.append(Paragraph("PROCURAÇÃO PARTICULAR", styles['Title']))
        procuracao.append(Spacer(1, 4*cm))
        procuracao.append(Paragraph(self.texto.texto_procuracao(), styles['CorpoTexto']))
        procuracao.append(Spacer(1, 12*cm))
        procuracao.append(self.tabela.tabela_assinatura(self.projeto.cliente.nome_cliente,self.projeto.cliente.cpf, self.data))
        
        self.doc.build(procuracao)
    
    def to_bytes(self):
        return self.buffer.getvalue()    

