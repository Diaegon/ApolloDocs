from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from api.database import get_session
from api.schemas.models import User
from api.schemas.projetos.completo import ProjetoTodos
from api.schemas.projetos.formularioenelce import ProjetoFormularioEnelCe
from api.schemas.projetos.memorial import ProjetoMemorial
from api.schemas.projetos.procuracao import ProjetoProcuracao
from api.schemas.projetos.unifilar import ProjetoUnifilar
from api.security import get_current_user
from api.services.all_docs_service import AllDocsService
from api.services.docs_service import DocsService

router = APIRouter(prefix="/docs", tags=["Documentos"])
Sessions = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/memorialdescritivo", status_code=201, response_model=None)
async def post_data_memorial(
    dados_entrada: ProjetoMemorial,
    current_user: CurrentUser,
):
    buffer = DocsService.generate_memorial(dados_entrada)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=memorial.pdf"},
    )


from api.schemas.projetos.memorial_v2 import ProjetoMemorialV2
@router.post("/v2/memorialdescritivo", status_code=201, response_model=None)
async def post_data_memorial_v2(
    dados_entrada: ProjetoMemorialV2,
    current_user: CurrentUser,
    session: Sessions,
):
    buffer = DocsService.generate_memorial_v2(dados_entrada, session)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=memorial_v2.pdf"},
    )


@router.post("/procuracao", status_code=201, response_model=None)
async def post_data_procuracao(
    projeto: ProjetoProcuracao,
    current_user: CurrentUser,
):
    buffer = DocsService.generate_procuracao(projeto)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=procuracao.pdf"},
    )


from api.schemas.projetos.unifilar_v2 import ProjetoUnifilarV2
@router.post("/v2/diagramaunifilar", status_code=201, response_model=None)
async def post_data_diagrama_unifilar_v2(
    dados_entrada: ProjetoUnifilarV2,
    current_user: CurrentUser,
    session: Sessions,
):
    buffer = DocsService.generate_diagrama_unifilar_v2(dados_entrada, session)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=diagrama_unifilar_v2.pdf"
        },
    )


@router.post("/diagramaunifilar", status_code=201, response_model=None)
async def post_data_diagrama_unifilar(
    dados: ProjetoUnifilar,
    current_user: CurrentUser,
):
    buffer = DocsService.generate_diagrama_unifilar(dados)

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
):
    buffer = DocsService.generate_formulario_enel(dados)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=formulario.pdf"},
    )


@router.post("/todos", status_code=201, response_model=None)
async def post_data_todos_documentos(
    dados: ProjetoTodos,
    current_user: CurrentUser,
):
    """
    Generates all four documents (Memorial Descritivo, Procuração,
    Diagrama Unifilar, Formulário ENEL-CE) from a single payload and
    returns them as a ZIP archive.
    """
    buffer = AllDocsService.generate_all(dados)

    return StreamingResponse(
        buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": "attachment; filename=documentos.zip"
        },
    )
