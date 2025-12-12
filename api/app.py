from typing import Union
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
 
from io import BytesIO

from src.buildingdocuments.memorialdescritivo import MemorialDescritivo
from src.buildingdocuments.procuracao import Procuracao
from src.createproject import ProjectFactory
from src.schemas.schemas import Cliente, EnderecoCliente, EnderecoObra, Projeto, ProjetoMemorial, ConfiguracaoSistema, ProjetoProcuracao
from src.factory.datas.creatememorialobject import ObjetosCalculados
from src.config import INPUTS_DIR
import json 



IMAGE_PATH = "apollodocs_image.png"
app = FastAPI(title="ApolloDocs API", version="1.0.0")

@app.get("/")
def landing_page():
    return FileResponse(path=IMAGE_PATH, media_type="image/png")

#FAZER UM SCHEMA SÓ PRO MEMORIAL.
@app.post("/memorialdescritivo", status_code=201, response_model= None)
async def post_data_memorial(projeto: ProjetoMemorial, sistema_instalado: ConfiguracaoSistema):
    projeto_retorno = ProjectFactory.factory(inputs=None, inputs_projeto=projeto.dict(),
                                              config_sistema=sistema_instalado.dict())
    retorno = ObjetosCalculados(projeto_retorno).construtor_dados_memorial() #O OBJETO DE RETORNO É UM OBJ DATACLASS
    
    pdf = MemorialDescritivo(retorno)
    pdf.gerar_memorial()

    buffer = BytesIO(pdf.to_bytes())
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=memorial.pdf"}
    )

@app.post("/procuracao", status_code=201, response_model= None)
async def post_data_procuracao(projeto: ProjetoProcuracao):
    pdf = Procuracao(projeto)
    pdf.gerar_procuracao()

    buffer = BytesIO(pdf.to_bytes())
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=procuracao.pdf"}
    )


