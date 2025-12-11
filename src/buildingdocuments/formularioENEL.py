import fitz
from src.factorys.factorydatas.factorydocumentdata import (inversor_total_unifilar, carga_cliente, tensao_local, inversor_total_unifilar, potencia_total_unifilar)
from src.utils.helpers import (cft_crea, data_de_hoje, uc_cliente, ramal_cliente, logradouro_obra, fornecimento_cliente, numero_obra, complemento_obra, cep_obra, bairro_obra, email_cliente, telefone_cliente, cpf_cliente, latitude_obra, longitude_obra,
                            classe_codigo,classe_cliente,fornecimento_cliente, projetista, projeto, data_de_hoje, nome_procurador, email_procurador, telefone_procurador, municipio_obra, logradouro_obra, numero_obra, complemento_obra, bairro_obra,
                            nome_cliente)


caminho_doc =   r'support-files\templates_formularios\formulario_microgeracaoENEL.pdf'  
caminho_doc_10kw = r'support-files\templates_formularios\formulario_microgeracaoENEL10kw.pdf'  
output_formulario = r'output\formulario.pdf'

def gerar_formulario():
    if inversor_total_unifilar / 1000 <= 10:
        pdf_base_formulario = caminho_doc
    else:
        pdf_base_formulario = caminho_doc_10kw

    def inserir_dados_no_formulario_10k(pdf_base, pdf_saida):
        doc = fitz.open(pdf_base)
        page = doc[0]
        #dados cliente
        #primeira linha
        page.insert_text((45, 100), f"{uc_cliente}", fontsize=7, fontname="helv", color=(0, 0, 0))
        page.insert_text((165, 100), "X", fontsize=9, fontname="helv", color=(0, 0, 0))
        page.insert_text((360, 100), f"{classe_codigo}", fontsize=8, fontname="helv", color=(0, 0, 0))
        page.insert_text((410, 100), f"{classe_cliente} {fornecimento_cliente}" , fontsize=7, fontname="helv", color=(0, 0, 0))
        #segunda linha
        page.insert_text((45, 110), f"{nome_cliente}", fontsize=7, fontname="helv", color=(0, 0, 0))
        #terceira linha
        page.insert_text((45, 118), f"{logradouro_obra}", fontsize=7, fontname="helv", color=(0, 0, 0))
        page.insert_text((270, 118), f"{numero_obra} {complemento_obra}", fontsize=7, fontname="helv", color=(0, 0, 0))
        page.insert_text((370, 118), f"{cep_obra} ", fontsize=7, fontname="helv", color=(0, 0, 0)) 
        #quarta linha
        page.insert_text((45, 128), f"{bairro_obra}", fontsize=7, fontname="helv", color=(0, 0, 0)) 
        page.insert_text((185, 128), f"{municipio_obra}", fontsize=7, fontname="helv", color=(0, 0, 0))
        page.insert_text((45, 138), f"{email_cliente}", fontsize=7, fontname="helv", color=(0, 0, 0))
        page.insert_text((45, 147), f"{telefone_cliente}", fontsize=7, fontname="helv", color=(0, 0, 0))
        page.insert_text((45, 156), f"{cpf_cliente}", fontsize=7, fontname="helv", color=(0, 0, 0))     

        #dados unidade consumidora
        #primeira linha
        page.insert_text((190, 183), f"{latitude_obra}", fontsize=6, fontname="helv", color=(0, 0, 0))
        page.insert_text((300, 183), f"{longitude_obra}", fontsize=6, fontname="helv", color=(0, 0, 0))    
        #segunda linha
        page.insert_text((70, 192), f"{carga_cliente}", fontsize=7, fontname="helv", color=(0, 0, 0))
        page.insert_text((340, 192), f"{tensao_local} V", fontsize=7, fontname="helv", color=(0, 0, 0))
        #terceira linha
        page.insert_text((360, 202), f"X", fontsize=7, fontname="helv", color=(0, 0, 0))
        #quarta linha
        if ramal_cliente == 'aereo':
            page.insert_text((165, 220), f"X", fontsize=7, fontname="helv", color=(0, 0, 0))
        else:
            page.insert_text((265, 220), f"X", fontsize=7, fontname="helv", color=(0, 0, 0))
        # Dados da geração
        #primeira linha
        if inversor_total_unifilar <= potencia_total_unifilar:    
            page.insert_text((100, 246), f"{inversor_total_unifilar / 1000}", fontsize=7, fontname="helv", color=(0, 0, 0))
        else:
            page.insert_text((100, 246), f"{potencia_total_unifilar / 1000}", fontsize=7, fontname="helv", color=(0, 0, 0)) 
        #Dados procurador
        #primeira linha
        page.insert_text((70, 455), f"{nome_procurador}", fontsize=7, fontname="helv", color=(0, 0, 0)) 
        page.insert_text((30, 465), f"{telefone_procurador}", fontsize=7, fontname="helv", color=(0, 0, 0))
        page.insert_text((30, 475), f"{email_procurador}", fontsize=7, fontname="helv", color=(0, 0, 0))
        page.insert_text((20, 492), "Fortaleza", fontsize=7, fontname="helv", color=(0, 0, 0))  
        page.insert_text((99, 492), f"{data_de_hoje.strftime("%d/%m/%Y")}", fontsize=12, fontname="helv", color=(0, 0, 0))  

        doc.save(pdf_saida)

    def inserir_dados_no_formulario(pdf_base,pdf_saida):
        doc = fitz.open(pdf_base)
        page = doc[0]
        #dados cliente
        #primeira linha
        page.insert_text((47, 119), f"{uc_cliente}", fontsize=7, fontname="helv", color=(0, 0, 0))
        page.insert_text((195, 119), "X", fontsize=9, fontname="helv", color=(0, 0, 0))
        page.insert_text((430, 119), f"{classe_codigo}", fontsize=8, fontname="helv", color=(0, 0, 0))
        page.insert_text((480, 119), f"{classe_cliente} {fornecimento_cliente}" , fontsize=7, fontname="helv", color=(0, 0, 0))
        #segunda linha
        page.insert_text((47, 134), f"{nome_cliente}", fontsize=7, fontname="helv", color=(0, 0, 0))
        #terceira linha
        page.insert_text((47, 148), f"{logradouro_obra}", fontsize=7, fontname="helv", color=(0, 0, 0))
        page.insert_text((318, 148), f"{numero_obra} {complemento_obra}", fontsize=7, fontname="helv", color=(0, 0, 0))
        page.insert_text((430, 148), f"{cep_obra} ", fontsize=7, fontname="helv", color=(0, 0, 0)) 
        #quarta linha
        page.insert_text((47, 160), f"{bairro_obra}", fontsize=7, fontname="helv", color=(0, 0, 0)) 
        page.insert_text((220, 160), f"{municipio_obra}", fontsize=7, fontname="helv", color=(0, 0, 0))
        page.insert_text((47, 174), f"{email_cliente}", fontsize=7, fontname="helv", color=(0, 0, 0))
        page.insert_text((47, 186), f"{telefone_cliente}", fontsize=7, fontname="helv", color=(0, 0, 0))
        page.insert_text((47, 200), f"{cpf_cliente}", fontsize=7, fontname="helv", color=(0, 0, 0))     

        #dados unidade consumidora
        #primeira linha
        page.insert_text((221, 230), f"{latitude_obra}", fontsize=6, fontname="helv", color=(0, 0, 0))
        page.insert_text((351, 230), f"{longitude_obra}", fontsize=6, fontname="helv", color=(0, 0, 0))    
    #segunda linha
        page.insert_text((75, 243), f"{carga_cliente}", fontsize=7, fontname="helv", color=(0, 0, 0))
        page.insert_text((390, 243), f"{tensao_local} V", fontsize=7, fontname="helv", color=(0, 0, 0))
        #terceira linha
        if fornecimento_cliente == 'monofasico':
            page.insert_text((195, 257), f"X", fontsize=7, fontname="helv", color=(0, 0, 0))
        else:
            page.insert_text((420, 257), f"X", fontsize=7, fontname="helv", color=(0, 0, 0))

        #quarta linha
        if ramal_cliente == 'aereo':
            page.insert_text((195, 285), f"X", fontsize=7, fontname="helv", color=(0, 0, 0))
        else:
            page.insert_text((310, 285), f"X", fontsize=7, fontname="helv", color=(0, 0, 0))
        # Dados da geração
        #primeira linha
        if inversor_total_unifilar <= potencia_total_unifilar:    
            page.insert_text((107, 317), f"{inversor_total_unifilar / 1000}", fontsize=7, fontname="helv", color=(0, 0, 0))
        else:
            page.insert_text((107, 317), f"{potencia_total_unifilar / 1000}", fontsize=7, fontname="helv", color=(0, 0, 0)) 
        page.insert_text((510, 345), f"X", fontsize=7, fontname="helv", color=(0, 0, 0))    
        #Dados procurador
        #primeira linha
        page.insert_text((75, 665), f"{nome_procurador}", fontsize=7, fontname="helv", color=(0, 0, 0)) 
        page.insert_text((35, 680), f"{telefone_procurador}", fontsize=7, fontname="helv", color=(0, 0, 0))
        page.insert_text((30, 695), f"{email_procurador}", fontsize=7, fontname="helv", color=(0, 0, 0))
        page.insert_text((20, 720), "Fortaleza", fontsize=7, fontname="helv", color=(0, 0, 0))  
        page.insert_text((102, 720), f"{data_de_hoje.strftime("%d/%m/%Y")}", fontsize=12, fontname="helv", color=(0, 0, 0))  

        doc.save(pdf_saida) 

    if inversor_total_unifilar / 1000 <= 10:
        inserir_dados_no_formulario(pdf_base_formulario,output_formulario)     
    else:
        inserir_dados_no_formulario_10k(pdf_base_formulario,output_formulario)