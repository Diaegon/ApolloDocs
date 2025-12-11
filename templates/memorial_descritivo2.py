from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from datetime import datetime
from dateutil.relativedelta import relativedelta
import locale
import matplotlib.pyplot as plt

import json


# vem uma def Criar_memorial() quando os dados forem inseridos
with open('input_solar.json', 'r') as f:
    inputs = json.load(f)
data_de_hoje = datetime.now()
data_futura = data_de_hoje+relativedelta(months=1)
locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
plt.rcParams['text.usetex'] = True # Ativar o uso do LaTeX real (MikTeX)
doc = SimpleDocTemplate("memorial_geracao_distribuida.pdf", pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
# Estilos personalizados
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TituloSecao',
                          fontSize=14,
                          leading=18,
                          spaceAfter=12,
                          fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='SubSecao',
                          fontSize=12,
                          leading=18,
                          spaceAfter=12,
                          fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='CorpoTexto',
                          fontSize=10,
                          leading=14,
                          spaceAfter=6,
                          fontName='Helvetica',
                          alignment=4,
                          firstLineIndent=36))
estilotabela = TableStyle([
    # Comandos de estilo vão aqui:  ('COMANDO', (col_inicio, linha_inicio), (col_fim, linha_fim), valor_do_comando)
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),  # Fonte do cabeçalho
    ('FONTSIZE', (0, 0), (-1, -1), 10),  # tamanho da fonte das linhas
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Grades da tabela
])
estilotabelaloc = TableStyle([
    # Comandos de estilo vão aqui:  ('COMANDO', (col_inicio, linha_inicio), (col_fim, linha_fim), valor_do_comando)
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),  # Fonte do cabeçalho
    ('FONTSIZE', (0, 0), (-1, -1), 10),  # tamanho da fonte das linhas
    ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grades da tabela
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('ALIGN', (0, 1), (0, -1), 'CENTER'),
    ('VALIGN', (0, 1), (0, -1), 'MIDDLE'),
    ('SPAN', (0, 0), (-1, 0)),
    ('SPAN', (0, 1), (0, -1))

])
estilo_tabela_parametros = TableStyle([# Comandos de estilo vão aqui:  ('COMANDO', (col_inicio, linha_inicio), (col_fim, linha_fim), valor_do_comando)
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey), #fundo do cabecalho
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),  # Fonte do cabeçalho
    ('FONTSIZE', (0, 0), (-1, -1), 10),  # tamanho da fonte das linhas
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)   
    ])

def linha_sumario(titulo, pagina, largura_pontilhado=80):
    """Retorna uma string formatada com pontilhado entre título e página"""
    max_linha = largura_pontilhado
    texto_base = f'{titulo} '
    dots = '.' * max(3, max_linha - len(texto_base) - len(str(pagina)))
    return f'{texto_base}{dots} {pagina}'
def add_page_number(canvas, doc):
    page_num = canvas.getPageNumber()
    text = f"Página {page_num}"
    canvas.setFont('Helvetica', 9)
    width, height = doc.pagesize
    canvas.drawCentredString(width / 2.0, 1.5 * cm, text)

#CALCULOS

potenciatotalpainel = inputs['dados_cliente']['quantidade_painel'] * inputs['painel']['potencia'] / 1000
potenciaefetiva = potenciatotalpainel * 0.745
energia_gerada = potenciaefetiva * 5.84 * 30
corrente_saida = inputs['inversor']['potencia'] / 220
tensao_queda = (200 * 0.0173 * 10 * corrente_saida) / (220 * inputs['inversor']['cabo']) 
resultado = inputs['dados_cliente']['energia'] / 720
fatordecarga = resultado / inputs['dados_cliente']['carga']


# Textos

def texto_introducao():
    return f"   O presente relatório técnico tem por objetivo apresentar o memorial descritivo \
                       para implantação de um Gerador Fotovoltaico de fabricação da <b>{inputs['inversor']['marca']} {inputs['inversor']['modelo']}</b>. \
                         Este modelo e quantidade de gerador foi previamente aprovado pelo proprietário da residência.\
                             Este gerador fotovoltaico se conectará ao sistema de baixa tensão, após a medição \
                                de energia da ENEL. O mesmo terá como objetivo suprir parte das cargas desta residencia. \
                                 A previsão de ligação do sistema elétrico é para <b>{data_futura.strftime("%d de %B de %Y")}</b>."
def texto_loc():
    return f"No diagrama de situação é ilustrada a planta de situação da residência onde será \
 implantado na {inputs['endereco']['logradouro']}, {inputs['endereco']['numero_casa']}  {inputs['endereco']['complemento']}, {inputs['endereco']['municipio']}, {inputs['endereco']['estado']}. A tabela 2.1 \
 mostra o georeferenciamento da localidade de instalação e do gerador."
def texto_loc2():
    return "A área de telhado da residência foi escolhida por apresentar vantagens de insolação \
 permanente durante todas as horas do dia para evitar o sombreamento dos painéis \
 fotovoltaicos e segurança dos equipamentos"
def texto_carginst():
    return f"A carga instalada é típica de um estabelecimento {inputs['dados_cliente']['classeconsumo']}, constituído de iluminação e \
 eletrodomésticos diversos, sendo {inputs['dados_cliente']['carga']} kW.  A energia \
 media de consumo é de  {inputs['dados_cliente']['energia']} kWh."
def texto_calculo_demanda():
    return "Considerando um mês comercial com 720 horas, pode-se calcular a demanda média \
 mensal através da equação:"
def texto_calculo_demanda2():
    return "Esta demanda média está dentro do limite da potência máxima injetada no sistema \
da ENEL, de acordo com a norma NT - 010."
def texto_calculo_fc():
    return "O fator de carga médio desta residência é calculado através da equação:"
def texto_geradorfv():
    return f"O Gerador Fotovoltaico escolhido para compor a geração suplementar da residência \
alvo deste projeto é composto de {inputs['dados_cliente']['quantidade_painel']} módulos Fotovoltaicos {inputs['painel']['marca']}  {inputs['painel']['modelo']} \
de {inputs['painel']['potencia']} Wp e {inputs['dados_cliente']['quantidade_inversor']}  inversor {inputs['inversor']['marca']} {inputs['inversor']['modelo']} . \
O   modulo   solar   fotovoltaico   monocristalino   ({inputs['painel']['potencia']} Wp)   possui   as   características \
técnicas   apresentado   na   tabela   a seguir.   Considerando   que   os   módulos   instalados   são   os   de \
{inputs['painel']['potencia']} , e que eles tem uma tensão elétrica de máxima potência (Vmp) de {inputs['painel']['vp']} Vmp. A \
solução prevista para ser instalada tem 1 arranjo com 6 módulos. Tendo um sistema total \
com {inputs['dados_cliente']['quantidade_painel']} módulos que resultam numa potência total de {potenciatotalpainel:.2f} kWp." 
#TEM QUE AJUSTAR A LÓGICA DESSA ULTIMA PARTE DOS ARRANJOS
def texto_potenciafv():
    return f"O georeferenciamento do local da instalação do Gerador Fotovoltaico estabelece o \
valor de 74,5% das Condições de Teste padrão (STC) do modulo Fotovoltaico. Por essa \
premissa,  terei   uma   Potencia   resultante   do  meu  Gerador  Fotovoltaico  (GF)  também   de \
74,5% da Potencia instalada ({potenciatotalpainel:.2f} kW). Assim, a Potencia efetiva do GF é de  {potenciaefetiva:.2f}kW, o\
que satisfaz a demanda média calculada."
def texto_calculo_enegiagerada():
    return f"Considerando a potência média disponível de  {potenciaefetiva:.2f} kW  e a média anual do ponto \
georeferenciado do sistema Horas de Sol a Pico (HSP) que é de 5,84 kWh/m2/dia, como \
parâmetro de medição da radiação solar em um mês comercial, pode-se calcular a energia \
média através do produto destas duas grandezas, que resulta em {energia_gerada:.0f} kWh."
def texto_diagramas():
    return "A figura a seguir apresenta o esquema básico de ligação de um Gerador Fotovoltaico. \
Nesta   figura   pode   ser   ver   todas   as   partes   que   compõem   o   sistema,   desde   o   Gerador \
Fotovoltaico até a conexão à carga e à rede."
def texto_parametrizacao():
    return "O inversor para cumprir sua função de proteção, é parametrizado com os seguintes \
valores, de modo a não exceder os limites recomendados pela norma NT – 010 Coelce."
def texto_instalacao():
    return "A residência é alimentada através da rede de baixa tensão da ENEL em 220V. O \
ponto de entrega se dá em um quadro instalado junto ao muro da propriedade."
def texto_diagramauni():
    return "O diagrama unifilar geral se encontra em anexo."
def texto_dimensionamento_protecao():
    return f"Este   Gerador   Fotovoltaico   será   conectado   ao   barramento   de   baixa   tensão   do \
consumidor, logo abaixo da proteção geral, que é constituída por um disjuntor {inputs['dados_cliente']['fornecimento']} \
de   {inputs['dados_cliente']['disjuntor_geral']}   A.   Por   sua   vez,   o   ramal   de   interligação   do   Gerador   Fotovoltaico   ao   quadro   de \
medição é feito por  um  disjuntor {inputs['inversor']['numero_fases']} {inputs['inversor']['protecao']} de A. Esta capacidade de condução foi \
calculada através da seguinte equação."
def texto_dimensionamento_protecao2():
    return f"A interligação entre o Gerador Fotovoltaico e o quadro de medição será feito através \
de um cabo de cobre flexível, isolado em PVC com uma seção reta de {inputs['inversor']['cabo']} mm², e sua \
proteção se dará através de um disjuntor de {inputs['inversor']['protecao']} A. \
O   dimensionamento   do   condutor   de   {inputs['inversor']['cabo']}  mm²   atende   aos   critérios   de   máxima \
capacidade de corrente, já que o mesmo tem capacidade térmica de conduzir até {inputs['inversor']['correntemax']} A; e \
atende também ao critério de máxima queda de tensão. \
Como trata-se da interligação de um gerador, a máxima queda de tensão permitida é \
de 3%. A equação abaixo apresenta o cálculo desta queda." 
def texto_dimensionamento_protecao3():
    return f"Introduzindo estes valores na equação anterior resulta em uma queda de tensão de {tensao_queda:.2f} %, o que satisfaz plenamente o limite máximo de queda que é de 3%."
def texto_disjuntores():
    return f"A proteção geral é feita através de um disjuntor {inputs['dados_cliente']['fornecimento']} de {inputs['dados_cliente']['disjuntor_geral']} A, com curva \
direta de atuação C, e o Gerador Fotovoltaico terá a sua proteção realizada por um disjuntor \
{inputs['inversor']['numero_fases']} de {inputs['inversor']['protecao']} A, curva de atuação B. A seletividade é garantida observando o valor \
maior de corrente nominal do disjuntor principal em relação ao disjuntor para proteção do \
cabo do inversor, e suas curvas de atuação."
def texto_sinalizacao():
    return "No padrão de entrada será instalada placa de sinalização, confeccionada em \
PVC 2,0 mm com tratamento anti-UV, conforme Figura a seguir, fixada de acordo \
com o desenho D010.01 dá NT Br-010 R-01, sem que haja a perfuração da caixa para \
fixação da sinalização. "

#falta resolver a parte da logica do programa

#IMAGENS
imagem1_caminho = 'diagramasolar.png'
img1 = Image(imagem1_caminho, width=10*cm, height=7*cm)

imagem2_caminho ='aviso.png'
img2 = Image(imagem2_caminho, width=18*cm, height=15*cm)

imagem3_caminho = 'ASSINATURA.png'
img3 = Image(imagem3_caminho, width=15*cm, height=4*cm)

#TABELAS 

dados = [[f"UC:{inputs['dados_cliente']['UC']}"], [f"Classe:{inputs['dados_cliente']['classeconsumo']}{inputs['dados_cliente']['fornecimento']} "], [f"Nome do Cliente: {inputs['dados_cliente']['nome']}"],
         [f"Endereço: {inputs['endereco']['logradouro']}, {inputs['endereco']['numero_casa']}  {inputs['endereco']['complemento']}, {inputs['endereco']['municipio']}, {inputs['endereco']['estado']}."],
         [f"CEP:{inputs['endereco']['CEP']}"],
         [f"CPF/CNPJ: {inputs['dados_cliente']['CPF']}"]]
tabeladedados = Table(dados)
tabeladedados.setStyle(estilotabela)

loc_instalacao = [["COORDENADAS - coordenadas decimais - WGS 84 "],
                  [" Local de implantação do Gerador fotovoltaico",
                      "Lat: ", "Long: "],
                  ["", f"{inputs['endereco']['latitude']}", f"{inputs['endereco']['longitude']}"]]
tabela_localizacao = Table(loc_instalacao)
tabela_localizacao.setStyle(estilotabelaloc)

modulo_caracteristicas = [["Potência nominal máx. (Pmax) ", f"{inputs['painel']['potencia']} Wp"],
                          ["Tensão operacional opt. (Vmp) ", f"{inputs['painel']['vp']} V"],
                            ["Corrente operacional opt. (Imp)", f"{inputs['painel']['imp']} A"], 
                            ["Tensão circuito aberto (Voc) ", f"{inputs['painel']['voc']} V"], 
                            ["Corrente curto-circuito (Isc)", f"{inputs['painel']['isc']} A"]]
tabelapainel = Table(modulo_caracteristicas)
tabelapainel.setStyle(estilotabela)

parametros_tensao_inversor = [["Faixa de tensão no ponto de conexão [V]","Tempo de desconexão [s]"], ["TL > 231","0,2 s"], ["189 ≤ TL ≤ 231","Operação Normal"], ["TL < 195,5","0,2 s"]]
tabela_parametros_tensao_inversor = Table(parametros_tensao_inversor)
tabela_parametros_tensao_inversor.setStyle(estilo_tabela_parametros)

parametros_frequencia_inversor = [["Faixa de freqüência no ponto de conexão (Hz)","Tempo de desconexão [s]"], ["f ≤ 57,5","0,2"],["59,9 < f ≤ 60,1","Operação normal"],["f > 62,5","0,2"] ]
tabela_parametros_frequencia_inversor = Table(parametros_frequencia_inversor)
tabela_parametros_frequencia_inversor.setStyle(estilo_tabela_parametros)

parametros_fp_inversor = [["Potência Nominal (W) - Pn","Faixa de fator de potência","Fator de potência \nconfiguração em fábrica"], [f"{inputs['inversor']['potencia']}","0,95 indutivo – 0,95 capacitivo","1"]]
tabela_parametros_fp_inversor = Table(parametros_fp_inversor)
tabela_parametros_fp_inversor.setStyle(estilo_tabela_parametros)

queda_tensao = [["ρ  - resistividade do cobre","0,0173"], [Paragraph("L<sub>c</sub> - comprimento do condutor",styles["CorpoTexto"]),"10 m"], 
                [Paragraph("I<sub>c</sub> - corrente do condutor",styles["CorpoTexto"]),f"{corrente_saida:.2f} A"], ["Cosφ - fator de potencia","1"], [Paragraph("S<sub>c</sub> - Seção reta do condutor",styles["CorpoTexto"]), f"{inputs['inversor']['cabo']} mm²"], 
                [Paragraph("V <sub>f</sub> - tensão ", styles["CorpoTexto"]), f"{inputs['inversor']['tensao']}"]]
tabela_queda_tensao = Table(queda_tensao)
tabela_queda_tensao.setStyle(estilotabela)

# EQUAÇÕES
#EQ.DEMANDA MEDIA
equacao = fr"$D_{{\mathrm{{media}}}} = \frac{{\mathrm{{Energia\ media}}}}{{N^{{\circ}}\,\mathrm{{de\ horas}}}} = \frac{{{inputs['dados_cliente']['energia']}}}{{720}} = {resultado:.2f}\ kW$"
#EQ.FATOR DE CARGA
equacao2 = fr"$FC = \frac{{\mathrm{{Energia}}}}{{\mathrm{{Potencia instalada \ x \ 720h}}}} = \frac{{{inputs['dados_cliente']['energia']}}}{{{inputs['dados_cliente']['carga']} \ x  \ 720}} = {fatordecarga:.2f}\ kW$"
#EQ. DISJUNTOR PROTECAO INVERSOR
equacao3 = fr"$I_{{\mathrm{{AG}}}} = \frac{{\mathrm{{potencia\ nominal}}}}{{\mathrm{{Tensao\ nominal}}}} = \frac{{{inputs['inversor']['potencia']}}}{{{inputs['inversor']['tensao']}}} = {corrente_saida:.2f}\ A$"
#EQ. QUEDA DE TENSÃO
equacao4 = fr"$\Delta V \% = \frac{{200*\rho*L_c*I_c*cos\varphi}}{{S_c*V_f}}$"


def render_equation_to_image(equation, filename):
    fig = plt.figure(figsize=(0.01, 0.01))
    plt.text(0.5, 0.5, f"${equation}$", fontsize=20, ha='center', va='center')
    plt.axis('off')
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.2, dpi=300)
    plt.close()
def insert_equation(equation, story, img_filename):
    render_equation_to_image(equation, img_filename)
    img = Image(img_filename)
    img.drawHeight = 50
    img.drawWidth = 150
    story.append(img)

"""procurar fazer com que as imagens das equações sejam salvas no buffer e apagadas logo em seguida"""
# Elementos do documento


story = []


# CAPA @@ NÃO MUDA NADA
story.append(Paragraph("MEMORIAL DESCRITIVO", styles['Title']))
story.append(Spacer(1, 2*cm))
story.append(Paragraph("PROJETO DE GERAÇÃO DISTRIBUÍDA", styles['Heading1']))
story.append(Spacer(1, 3*cm))
story.append(Paragraph(f" PROJETO PARA IMPLANTAÇÃO DE GERADOR FOTOVOLTAICO NA ÁREA {inputs['dados_cliente']['classeconsumo']} DO(A) Cliente: {inputs['dados_cliente']['nome']}", styles['Heading3']))
story.append(Paragraph(f"Local: {inputs['endereco']['municipio']}", styles['Heading3']))
story.append(Paragraph(f"{data_de_hoje.strftime("%d/%m/%Y")}", styles['Heading4']))
story.append(PageBreak())

#SUMARIO @@NÂO MUDA NADA

story.append(Paragraph('SUMÁRIO', styles['TituloSecao']))
story.append(Spacer(1, 2*cm))
topicos = [
    ('1 - INTRODUÇÃO', 3),
    ('1.1 - Identificação do cliente', 3),
    ('2 - LOCALIZAÇÃO DO GERADOR FOTOVOLTAICO', 3),
    ('2.1 - Planta de situação do gerador', 3),
    ('3 -CARGA INSTALADA ',4),
    ('3.1 - Cálculo da Demanda Média',4),
    ('3.2 - Cálculo do Fator de Carga Médio',4),
    ('4 - GERADOR FOTOVOLTAICO',4),
    ('4.1 - Cálculo da Energia Média Gerad5',5),
    ('5 - DIAGRAMAS BÁSICOS',5),
    ('5.1 - Parametrização do inverso',5),
    ('5.1.x - tabelas de parametrização do inversor',6),
    ('6 - INSTALAÇÃO ELÉTRICA',6),
    ('6.1 – Diagrama unifilar Geral',6),
    ('6.2 – Dimensionamento da Proteção',6),
    ('6.3 – Coordenação entre os Disjuntores',7),
    ('7 – SINALIZAÇÃO',7),
    ('8 – RESPONSÁVEL TÉCNICO',7),
]
for titulo, pagina in topicos:
    linha = linha_sumario(titulo, pagina)
    story.append(Paragraph(linha, styles['SubSecao']))

story.append(PageBreak())
#DOC
story.append(Paragraph("1 - INTRODUÇÃO", styles['TituloSecao']))
story.append(Spacer(1, 1*cm))
story.append(Paragraph(texto_introducao(), styles['CorpoTexto']))
story.append(Spacer(1, 1*cm))
story.append(Paragraph("1.1 - Identificação do cliente", styles['SubSecao']))
story.append(tabeladedados)
story.append(Spacer(1, 2*cm))
story.append(Paragraph("2 - LOCALIZAÇÃO DO GERADOR FOTOVOLTAICO", styles['TituloSecao']))
story.append(Spacer(1, 1*cm))
story.append(Paragraph("2.1 -Planta de situação do gerador", styles['SubSecao']))
story.append(Paragraph(texto_loc(), styles['CorpoTexto']))
story.append(tabela_localizacao)
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph(texto_loc2(), styles['CorpoTexto']))
story.append(PageBreak())
story.append(Paragraph("3 - CARGA INSTALADA", styles['TituloSecao']))
story.append(Spacer(1, 2*cm))
story.append(Paragraph(texto_carginst(), styles['CorpoTexto']))
story.append(Spacer(1, 1*cm))
story.append(Paragraph("3.1 - Cálculo da Demanda Média", styles['SubSecao']))
story.append(Paragraph(texto_calculo_demanda(), styles['CorpoTexto']))
insert_equation(equacao,story,'eqdemanda.png')
story.append(Paragraph(texto_calculo_demanda2(), styles['CorpoTexto']))
story.append(Spacer(1, 1*cm))
story.append(Paragraph("3.2 - Cálculo do Fator de Carga Médio", styles['SubSecao']))
story.append(Paragraph(texto_calculo_fc(), styles['CorpoTexto']))
insert_equation(equacao2,story,'eqfc.png')
story.append(Spacer(1, 1*cm))
story.append(Paragraph("4 - GERADOR FOTOVOLTAICO", styles['TituloSecao']))
story.append(Spacer(1, 1*cm))
story.append(Paragraph(texto_geradorfv(), styles['CorpoTexto']))
story.append(tabelapainel)
story.append(Paragraph(texto_potenciafv(), styles['CorpoTexto']))
story.append(Spacer(1, 1*cm))
story.append(Paragraph("4.1 - Cálculo da Energia Média Gerada ", styles['SubSecao']))
story.append(Paragraph(texto_calculo_enegiagerada(), styles['CorpoTexto']))
story.append(Spacer(1, 2*cm))
story.append(Paragraph("5 - DIAGRAMAS BÁSICOS", styles['TituloSecao']))
story.append(Spacer(1, 1*cm))
story.append(Paragraph(texto_diagramas(), styles["CorpoTexto"]))             
story.append(img1)
story.append(Spacer(1, 1*cm))
story.append(Paragraph("5.1 - Parametrização do inversor ", styles['SubSecao']))
story.append(Spacer(1, 1*cm))
story.append(Paragraph(texto_parametrizacao(), styles["CorpoTexto"]))
story.append(Spacer(1, 2*cm))
story.append(Paragraph("5.1.1 - Ajuste de sobre e Subtensão ", styles['SubSecao']))
story.append(tabela_parametros_tensao_inversor)
story.append(Spacer(1, 1*cm))
story.append(Paragraph("5.1.2 - Ajustes dos Limites de Freqüência (sobre e subfreqüência) ", styles['SubSecao']))
story.append(tabela_parametros_frequencia_inversor)
story.append(Spacer(1, 1*cm))
story.append(Paragraph(" 5.1.3 - Ajustes do Limite do Fator de Potência", styles['SubSecao']))
story.append(tabela_parametros_fp_inversor)
story.append(Spacer(1, 2*cm))
story.append(Paragraph("6 - INSTALAÇÃO ELÉTRICA", styles['TituloSecao']))
story.append(Paragraph(texto_instalacao(), styles['CorpoTexto']))
story.append(Spacer(1, 1*cm))
story.append(Paragraph(" 6.1 – Diagrama unifilar Geral", styles['SubSecao']))
story.append(Paragraph(texto_diagramauni(), styles["CorpoTexto"]))
story.append(Spacer(1, 1*cm))
story.append(Paragraph(" 6.2 – Dimensionamento da Proteção e Alimentação do Gerador Fotovoltaico", styles['SubSecao']))
story.append(Paragraph(texto_dimensionamento_protecao(), styles['CorpoTexto']))
insert_equation(equacao3,story,'corrente.png')
story.append(Spacer(1, 1*cm))
story.append(Paragraph(texto_dimensionamento_protecao2(), styles['CorpoTexto']))
insert_equation(equacao4,story,'quedatensao.png')
story.append(Spacer(1, 1*cm))
story.append(tabela_queda_tensao)
story.append(Spacer(1, 1*cm))
story.append(Paragraph(texto_dimensionamento_protecao3(), styles['CorpoTexto']))
story.append(Paragraph(" 6.3 – Coordenação entre o Disjuntor do Gerador Fotovoltaico e da Proteção Geral", styles['SubSecao']))
story.append(Spacer(1, 1*cm))
story.append(Paragraph(texto_disjuntores(), styles["CorpoTexto"]))
story.append(Spacer(1, 2*cm))
story.append(Paragraph("7 – SINALIZAÇÃO", styles['TituloSecao']))
story.append(Paragraph(texto_sinalizacao(), styles["CorpoTexto"]))
story.append(img2)
story.append(Spacer(1, 2*cm))
story.append(Paragraph("8 – RESPONSÁVEL TÉCNICO", styles['TituloSecao']))
story.append(Spacer(1, 3*cm))
story.append(img3)

doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
