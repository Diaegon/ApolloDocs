from http import HTTPStatus
from io import BytesIO
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from api.database import get_session
from api.schemas.models import User
from api.schemas.projetos.formularioenelce import ProjetoFormularioEnelCe
from api.schemas.projetos.memorial import ProjetoMemorial
from api.schemas.projetos.procuracao import ProjetoProcuracao
from api.schemas.projetos.unifilar import ProjetoUnifilar
from api.security import get_current_user
from src.buildingdocuments.formularioENEL import FormularioEnelCe
from src.buildingdocuments.memorialdescritivo import MemorialDescritivo
from src.buildingdocuments.procuracao import Procuracao
from src.buildingdocuments.unifilar import DiagramaUnifilar
from src.createproject import ProjectFactory
from src.domain.creatediagramobject import ObjetoDiagramaUnifilar
from src.domain.creatememorialobject import ObjetosCalculados

router = APIRouter(prefix="/docs", tags=["Documentos"])
Sessions = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


# FAZER UM SCHEMA SÓ PRO MEMORIAL.
@router.post("/memorialdescritivo", status_code=201, response_model=None)
async def post_data_memorial(
    dados_entrada: ProjetoMemorial,
    current_user: CurrentUser,
    user_id: int,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not enough permissions"
        )

    projeto = ProjectFactory.factory(dados_entrada)
    retorno = ObjetosCalculados(
        projeto
    )  # O OBJETO DE RETORNO É UM OBJ DATACLASS
    print("\n")
    retorno = retorno.construtor_dados_memorial()
    pdf = MemorialDescritivo(retorno)
    pdf.gerar_memorial()

    buffer = BytesIO(pdf.to_bytes())
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=memorial.pdf"},
    )


@router.post("/procuracao", status_code=201, response_model=None)
async def post_data_procuracao(
    projeto: ProjetoProcuracao,
    current_user: CurrentUser,
    user_id: int,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not enough permissions"
        )

    pdf = Procuracao(projeto)
    pdf.gerar_procuracao()

    buffer = BytesIO(pdf.to_bytes())
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=procuracao.pdf"},
    )


@router.post("/diagramaunifilar", status_code=201, response_model=None)
async def post_data_diagrama_unifilar(
    dados: ProjetoUnifilar,
    current_user: CurrentUser,
    user_id: int,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not enough permissions"
        )

    projeto = ObjetoDiagramaUnifilar(dados).construir_dados_diagrama()
    pdf = DiagramaUnifilar(projeto)
    pdf.gerar_diagrama()
    buffer = BytesIO(pdf.to_bytes())
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=diagrama_unifilar.pdf"
        },
    )


@router.post("/formularioenel", status_code=201, response_model=None)
async def post_data_formulario_enel_ce(
    dados: ProjetoFormularioEnelCe,
    current_user: CurrentUser,
    user_id: int,
):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not enough permissions"
        )

    pdf = FormularioEnelCe(dados)
    pdf.gerar_formulario()

    buffer = BytesIO(pdf.to_bytes())
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=formulario.pdf"},
    )


# CRIAR UM ENDPOINT PARA GERAÇÃO DE CONTRATOS COM AJUSTE DE IA########
