from typing import Union
from fastapi import FastAPI
from fastapi.responses import FileResponse

from src.factorys.datas.createproject import ProjectFactory
from src.factorys.datas.objectbuider import ObjetosCalculados
from src.config import INPUTS_DIR
import json 


file = INPUTS_DIR / "input_solar.json"
file2 = INPUTS_DIR / "input_necessario.json"
inputs = json.loads(file.read_text(encoding="utf-8"))
inputs_projeto = json.loads(file2.read_text(encoding="utf-8"))

projeto = ProjectFactory.factory(inputs, inputs_projeto)
retorno = ObjetosCalculados(projeto).construtor_dados_memorial()



app = FastAPI()

@app.get("/")
def read_root():
    recebe = retorno
    return recebe

@app.get("/pdf-memorial")
def get_pdf_memorial():
    pdf_path = "output/diagrama.pdf"
    
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename="resultado.pdf"
    )

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

