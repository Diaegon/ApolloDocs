#transferir para um fazedor de texto.

texto_disjuntorgeral_unifilar = f"DISJUNTOR\nMONOFÁSICO\n \n{projeto.disjuntor_geral} A - 220V" 
texto2_disjuntorgeral_unifilar = f"DISJUNTOR\nTRIFÁSICO\n \n{projeto.disjuntor_geral} A - 380/220V" 

#texto disjuntor unifilar
texto_disjuntor1_unifilar = f"DISJUNTOR\nMONOFÁSICO\n{disjuntor_protecao1} A - 220V"
texto2_disjuntor1_unifilar = f"DISJUNTOR\nTRIFÁSICO\n{disjuntor_protecao1} A - 380V"

#texto inversor diagrama unifilar
inversor_diagrama = f"{quantidade_inversor}x " + f" {inversor_marca} \n {inversor_modelo}"
