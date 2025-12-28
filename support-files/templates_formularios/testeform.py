import fitz  # PyMuPDF

doc = fitz.open("formularioinferior10k.pdf")
page = doc[0]

def preencher_por_frase(page, frase, valor, dy=-1):
    areas = page.search_for(frase)
    if not areas:
        print(f"Frase não encontrada: {frase}")
        return

    rect = areas[0]

    x = rect.x1 + 2
    y = rect.y0 + rect.height + dy

    page.insert_text(
        (x, y),
        valor,
        fontsize=9,
        fontname="helv"
    )

CAMPOS_UC = {
    "Código da UC:": "teste",
    "Titular da UC :": "teste",
    "Rua/Av.:": "teste",
    "Nº:": "teste",
    "CEP:": "teste",
    "Bairro:": "teste",
    "Cidade:": "teste",
    "E-mail:": "teste",
    "Telefone:": "teste",
    "Celular:": "teste",
    "CNPJ/CPF:": "teste",
    "Latitude:": "TESTE",
    "Longitude:": "TESTE",
    "Potência instalada (kW):": "TESTE",
    "Tensão de atendimento (V):": "TESTE",
    "Potência instalada de geração (kW):": "TESTE",
    "Outra (especificar):": "TESTE",

}

CAMPOS_SOLICITANTE = {
    "Nome/Procurador Legal:": "TESTE",
    "Telefone:": "TESTE",
    "E-mail:": "TESTE",
}

CAMPOS_ASSINATURA = {
    "Local": "TESTE",
    "Data": "TESTE",
}



for frase, valor in CAMPOS_UC.items():
    preencher_por_frase(page, frase, valor)

# for frase, valor in CAMPOS_ASSINATURA.items():
#     preencher_por_frase(page, frase, valor)

# for frase, valor in CAMPOS_SOLICITANTE.items():
#     preencher_por_frase(page, frase, valor)
doc.save("preenchido.pdf")