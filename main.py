import json
from src.gerar_pdf import gerar_memorial, gerar_procuracao
from src.unifilar import gerar_diagramaunifilar
from src.formularioENEL import gerar_formulario
from src.config import INPUTS_DIR


caminho_absoluto = INPUTS_DIR / "input_solar.json"

with open(caminho_absoluto, 'r', encoding='utf-8') as f:
    inputs = json.load(f)

def gerar_projeto():
    gerar_memorial(inputs)
    gerar_procuracao(inputs)
    gerar_diagramaunifilar()
    gerar_formulario()

gerar_projeto()