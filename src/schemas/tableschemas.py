from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import TableStyle, Table
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak        


styles = getSampleStyleSheet()
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
estilo_assinatura = TableStyle([
    ('GRID', (0, 0), (0, 0), 1, colors.black),

    ('ALIGN', (0, 0), (-1, -1), 'CENTER')
])

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
