from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
 
from io import BytesIO

from src.buildingdocuments.memorialdescritivo import MemorialDescritivo
from src.buildingdocuments.procuracao import Procuracao
from src.buildingdocuments.unifilar import DiagramaUnifilar
from src.createproject import ProjectFactory
from src.schemas.schemas import ProjetoMemorial, ProjetoProcuracao, ProjetoUnifilar
from src.factory.datas.creatememorialobject import ObjetosCalculados
from src.factory.datas.creatediagramobject import ObjetoDiagramaUnifilar
from src.config import INPUTS_DIR
import json 



IMAGE_PATH = "apollodocs_image.png"
app = FastAPI(title="ApolloDocs API", version="1.0.0")

@app.get("/")
def landing_page():
    return FileResponse(path=IMAGE_PATH, media_type="image/png")

#FAZER UM SCHEMA SÓ PRO MEMORIAL.
@app.post("/memorialdescritivo", status_code=201, response_model= None)
async def post_data_memorial(dados_entrada: ProjetoMemorial):
    projeto = ProjectFactory.factory(dados_entrada)

    print(projeto)
    retorno = ObjetosCalculados(projeto) #O OBJETO DE RETORNO É UM OBJ DATACLASS
    print("\n")
    retorno = retorno.construtor_dados_memorial()
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

@app.post("/diagramaunifilar", status_code=201, response_model= None)
async def post_data_diagrama_unifilar(dados: ProjetoUnifilar):
    projeto = ObjetoDiagramaUnifilar(dados).construir_dados_diagrama()
    pdf = DiagramaUnifilar(projeto)
    pdf.gerar_diagrama()
    buffer = BytesIO(pdf.to_bytes())
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=diagrama_unifilar.pdf"}
    )


#####CRIAR UM ENDPOINT PARA GERAÇÃO DE CONTRATOS COM AJUSTE DE IA########