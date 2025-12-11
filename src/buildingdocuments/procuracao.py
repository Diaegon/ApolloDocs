from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from src.schemas.tableschemas import styles

def gerar_procuracao():
    proc = SimpleDocTemplate(r"procuracao.pdf", pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    procuracao = []
    procuracao.append(Paragraph("PROCURAÇÃO PARTICULAR", styles['Title']))
    procuracao.append(Spacer(1, 4*cm))
    procuracao.append(Paragraph(texto.texto_procuracao(), styles['CorpoTexto']))
    procuracao.append(Spacer(1, 12*cm))
    procuracao.append(tabela.tabela_assinatura(projeto.cliente.nome_cliente,projeto.cliente.cpf, retorno.data_de_hoje().date()))
    proc.build(procuracao)

if __name__ == "__main__":
    from src.factorys.datas.createproject import ProjectFactory
    from src.config import INPUTS_DIR
    from src.factorys.texts.text_procuracao import TextoProcuracao
    from src.factorys.components.tables import TablesBuilder
    import json 
    from src.factorys.datas.objectbuider import ObjetosCalculados
    file = INPUTS_DIR / "input_solar.json"
    inputs = json.loads(file.read_text(encoding="utf-8"))
    
    projeto = ProjectFactory.factory(inputs)
    texto = TextoProcuracao(projeto)
    retorno = ObjetosCalculados(projeto)
    tabela = TablesBuilder(projeto)
    print(projeto.data_projeto)
    gerar_procuracao()
    