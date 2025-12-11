from typing import Union
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
 
from io import BytesIO

from src.buildingdocuments.memorialdescritivo import MemorialDescritivo
from src.createproject import ProjectFactory
from src.schemas.schemas import Cliente, EnderecoCliente, EnderecoObra, Projeto, ProjetoTeste, ConfiguracaoSistema
from src.factory.datas.creatememorialobject import ObjetosCalculados
from src.config import INPUTS_DIR
import json 



IMAGE_PATH = "apollodocs_image.png"
app = FastAPI()

@app.get("/")
def read_root():
    return FileResponse(path=IMAGE_PATH, media_type="image/png")


@app.post("/input")
async def post_data(projeto: ProjetoTeste, sistema_instalado: ConfiguracaoSistema):
    projeto_retorno = ProjectFactory.factory(inputs=None, inputs_projeto=projeto.dict(),
                                              config_sistema=sistema_instalado.dict())
    retorno = ObjetosCalculados(projeto_retorno).construtor_dados_memorial()
    
    pdf = MemorialDescritivo(retorno)
    pdf.gerar_memorial()

    buffer = BytesIO(pdf.to_bytes())
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=memorial.pdf"}
    )


def get_pdf_memorial(
):
    pdf_path = "output/diagrama.pdf"
    
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename="resultado.pdf"
    )



