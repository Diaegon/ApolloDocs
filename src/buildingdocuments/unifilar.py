import fitz
from src.factorys.factorydatas.factorydocumentdata import (quantidade_inversor, quantidade_inversor2, quantidade_inversor3, paineis_diagrama,  inversor_diagrama,  potencia_total_unifilar, 
                            cabo_inversor1, inversor_tensao,  texto_disjuntor1_unifilar, texto2_disjuntor1_unifilar, disjuntor_geral, quantidade_total_painel, 
                            inversor_total_unifilar, tensao_local, texto2_disjuntorgeral_unifilar, texto_disjuntorgeral_unifilar)
if quantidade_inversor2 not in [None,0]:
    from src.factorys.factorydatas.factorydocumentdata import (paineis_diagrama2, inversor2_diagrama,cabo_inversor2, inversor_tensao2,texto_disjuntor2_unifilar,texto2_disjuntor2_unifilar,)
if quantidade_inversor3 not in [None,0]:
    from src.factorys.factorydatas.factorydocumentdata import (paineis_diagrama3,inversor3_diagrama,cabo_inversor3,inversor_tensao3,texto_disjuntor3_unifilar,texto2_disjuntor3_unifilar)

from src.utils.helpers import (cft_crea, projetista, projeto, data_de_hoje, municipio_obra, logradouro_obra, numero_obra, complemento_obra, bairro_obra,
                            nome_cliente)


from io import BytesIO

def gerar_diagramaunifilar():
    caminho_inversor1 =   r'support-files\templates_diagramaunifilar\diagrama1.pdf'  
    caminho_inversor2 = r'support-files\templates_diagramaunifilar\diagrama2.pdf'
    caminho_inversor3 = r'support-files\templates_diagramaunifilar\diagrama3.pdf'
    caminho_output = r'output\diagrama.pdf'

    if quantidade_inversor not in [None,0]:
        pdf_base = caminho_inversor1
    if quantidade_inversor2 not in [None,0]:
        pdf_base = caminho_inversor2
    if quantidade_inversor3 not in [None,0]:
        pdf_base = caminho_inversor3 





    def inserir_dados_no_pdf(pdf_base, pdf_saida):
        doc = fitz.open(pdf_base)
        page = doc[0]  # primeira página  
        
        def funcao_dados_gerais():
            #dados {proprietario}
            page.insert_text((1245, 920), f"{nome_cliente}", fontsize=5, fontname="helv", color=(0, 0, 0))
            page.insert_text((1245, 1035), f"{logradouro_obra}, {numero_obra} {complemento_obra}, {bairro_obra}, {municipio_obra}.", fontsize=5, fontname="helv", color=(0, 0, 0))
            #DADOS PROJETISTA
            page.insert_text((1245, 785), f"ELETROTÉCNICO: {projetista}", fontsize=5, fontname="helv", color=(0, 0, 0))
            page.insert_text((1245, 790), f"CFT: {cft_crea}", fontsize=5, fontname="helv", color=(0, 0, 0))
            page.insert_text((1245, 937), f"{projeto}", fontsize=5, fontname="helv", color=(0, 0, 0))
            page.insert_text((1335, 937), f"{data_de_hoje.strftime("%d/%m/%Y")}", fontsize=5, fontname="helv", color=(0, 0, 0))
            page.insert_text((1375, 937), f"{municipio_obra}", fontsize=5, fontname="helv", color=(0, 0, 0))
            page.insert_text((1315, 230), f"{potencia_total_unifilar / 1000} kWp / {inversor_total_unifilar / 1000} kW", fontsize=12, fontname="helv", color=(0, 0, 0))
        funcao_dados_gerais()    
        
        def funcao_lado_do_inversor():
        #texto Paineis
            page.insert_text((370, 570), f"{paineis_diagrama}", fontsize=12, fontname="helv", color=(0, 0, 0))
            #texto inversores
            page.insert_text((553, 503), f"{inversor_diagrama}", fontsize=8, fontname="helv", color=(0, 0, 0))
            page.insert_text((643, 507), f"{cabo_inversor1} mm²", fontsize=8, fontname="helv", color=(0, 0, 0))
            if inversor_tensao == 220:
                page.insert_text((680, 555), f"{texto_disjuntor1_unifilar}", fontsize=6, fontname="helv", color=(0, 0, 0))
            elif inversor_tensao == 380:
                page.insert_text((680, 555), f"{texto2_disjuntor1_unifilar}", fontsize=6, fontname="helv", color=(0, 0, 0))
                #linhas do cabo
                page.draw_line(p1=(652, 534), p2=(652, 545), color=(0, 0, 0), width= 0.5)
                page.draw_line(p1=(648, 534), p2=(648, 545), color=(0, 0, 0), width= 0.5)
                #linhas do disjuntor
                page.draw_line(p1=(696, 530), p2=(696, 536), color=(0, 0, 0), width= 0.5)
                page.draw_line(p1=(700, 530), p2=(700, 536), color=(0, 0, 0), width= 0.5)  
        
        def funcao_lado_do_inversor2():
            page.insert_text((370, 450), f"{paineis_diagrama2}", fontsize=12, fontname="helv", color=(0, 0, 0))
            #texto inversores
            page.insert_text((528, 383), f"{inversor2_diagrama}", fontsize=8, fontname="helv", color=(0, 0, 0))
            page.insert_text((618, 387), f"{cabo_inversor2} mm²", fontsize=8, fontname="helv", color=(0, 0, 0))
            if inversor_tensao2 == 220:
                page.insert_text((660, 435), f"{texto_disjuntor2_unifilar}", fontsize=6, fontname="helv", color=(0, 0, 0))
            elif inversor_tensao2 == 380:
                page.insert_text((660, 435), f"{texto2_disjuntor2_unifilar}", fontsize=6, fontname="helv", color=(0, 0, 0))
                #linhas do cabo
                page.draw_line(p1=(626, 416), p2=(626, 427), color=(0, 0, 0), width= 0.5)
                page.draw_line(p1=(621, 416), p2=(621, 427), color=(0, 0, 0), width= 0.5)
                #linhas do disjuntor
                page.draw_line(p1=(671, 412), p2=(671, 419), color=(0, 0, 0), width= 0.5)
                page.draw_line(p1=(676, 412), p2=(676, 419), color=(0, 0, 0), width= 0.5)  
        
        def funcao_lado_do_inversor3():
            page.insert_text((370, 330), f"{paineis_diagrama3}", fontsize=12, fontname="helv", color=(0, 0, 0))
            #texto inversores
            page.insert_text((528, 263), f"{inversor3_diagrama}", fontsize=8, fontname="helv", color=(0, 0, 0))
            page.insert_text((618, 267), f"{cabo_inversor3} mm²", fontsize=8, fontname="helv", color=(0, 0, 0))
            if inversor_tensao3 == 220:
                page.insert_text((660, 315), f"{texto_disjuntor3_unifilar}", fontsize=6, fontname="helv", color=(0, 0, 0))
            elif inversor_tensao3 == 380:
                page.insert_text((660, 315), f"{texto2_disjuntor3_unifilar}", fontsize=6, fontname="helv", color=(0, 0, 0))
                #linhas do cabo
                page.draw_line(p1=(626, 298), p2=(626, 309), color=(0, 0, 0), width= 0.5)
                page.draw_line(p1=(621, 298), p2=(621, 309), color=(0, 0, 0), width= 0.5)
                #linhas do disjuntor
                page.draw_line(p1=(671, 294), p2=(671, 301), color=(0, 0, 0), width= 0.5)
                page.draw_line(p1=(676, 294), p2=(676, 301), color=(0, 0, 0), width= 0.5) 
        
        def funcao_lado_rede():
            if tensao_local == 220:
                page.insert_text((860, 555), f"{texto_disjuntorgeral_unifilar}", fontsize=6, fontname="helv", color=(0, 0, 0))
                page.insert_text((925, 555), "MEDIDOR\nMONOFÁSICO", fontsize=6, fontname="helv", color=(0, 0, 0))
            elif tensao_local == 380:
                page.insert_text((860, 555), f"{texto2_disjuntorgeral_unifilar}", fontsize=6, fontname="helv", color=(0, 0, 0))
                page.insert_text((925, 555), "MEDIDOR\nTRIFÁSICO", fontsize=6, fontname="helv", color=(0, 0, 0))
                #linhas do disjuntor
                page.draw_line(p1=(880, 530), p2=(880, 537), color=(0, 0, 0), width= 0.5)
                page.draw_line(p1=(886, 530), p2=(886, 537), color=(0, 0, 0), width= 0.5)
                #LINHAS DO CABO
                page.draw_line(p1=(773, 536), p2=(773, 547), color=(0, 0, 0), width= 0.5)
                page.draw_line(p1=(770, 536), p2=(770, 547), color=(0, 0, 0), width= 0.5)    
        
        if quantidade_inversor2 not in [None,0]:
            funcao_lado_do_inversor2()
        if quantidade_inversor3 not in [None,0]:
            funcao_lado_do_inversor3()
        funcao_lado_do_inversor()
        funcao_lado_rede()
    
        
        doc.save(pdf_saida)    



    inserir_dados_no_pdf(pdf_base, caminho_output)