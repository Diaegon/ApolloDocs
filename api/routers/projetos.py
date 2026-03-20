from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.database import get_session
from api.schemas.models import Cliente, Projeto, Procurador, Projetista, User
from api.schemas.pageschema import FilterPage
from api.schemas.projetos.projeto import ProjetoList, ProjetoPublic, ProjetoSchema
from api.security import get_current_user
from api.schemas.user import Message

router = APIRouter(prefix="/projetos", tags=["Projetos"])
Sessions = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
filtered_page = Annotated[FilterPage, Query()]

def _validate_relations(obj: ProjetoSchema, session: Session, user_id: int):
    # Check cliente
    if obj.cliente_id:
        c = session.scalar(select(Cliente).where((Cliente.id_cliente == obj.cliente_id) & (Cliente.user_id == user_id)))
        if not c:
            raise HTTPException(404, "Cliente not found or forbidden")
    # Check procurador
    if obj.procurador_id:
        p = session.scalar(select(Procurador).where((Procurador.id_procurador == obj.procurador_id) & (Procurador.user_id == user_id)))
        if not p:
            raise HTTPException(404, "Procurador not found or forbidden")
    # Check projetista
    if obj.projetista_id:
        pj = session.scalar(select(Projetista).where((Projetista.id_projetista == obj.projetista_id) & (Projetista.user_id == user_id)))
        if not pj:
            raise HTTPException(404, "Projetista not found or forbidden")

@router.post("/", status_code=HTTPStatus.CREATED, response_model=ProjetoPublic)
def create_projeto(projeto: ProjetoSchema, session: Sessions, current_user: CurrentUser):
    _validate_relations(projeto, session, current_user.id)
    db_obj = Projeto(**projeto.model_dump(), user_id=current_user.id)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

@router.get("/", response_model=ProjetoList)
def read_projetos(session: Sessions, current_user: CurrentUser, filter_page: filtered_page):
    objs = session.scalars(
        select(Projeto)
        .where(Projeto.user_id == current_user.id)
        .offset(filter_page.offset)
        .limit(filter_page.limit)
    ).unique().all()
    return {"projetos": objs}

@router.get("/{obj_id}", response_model=ProjetoPublic)
def read_projeto(obj_id: int, session: Sessions, current_user: CurrentUser):
    db_obj = session.scalar(
        select(Projeto).where(
            (Projeto.id_projeto == obj_id) & (Projeto.user_id == current_user.id)
        )
    )
    if not db_obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Projeto not found")
    return db_obj

@router.put("/{obj_id}", response_model=ProjetoPublic)
def update_projeto(obj_id: int, projeto: ProjetoSchema, session: Sessions, current_user: CurrentUser):
    db_obj = session.scalar(
        select(Projeto).where(
            (Projeto.id_projeto == obj_id) & (Projeto.user_id == current_user.id)
        )
    )
    if not db_obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Projeto not found")
    
    _validate_relations(projeto, session, current_user.id)
    for key, value in projeto.model_dump().items():
        setattr(db_obj, key, value)
    
    session.commit()
    session.refresh(db_obj)
    return db_obj

@router.delete("/{obj_id}", response_model=Message)
def delete_projeto(obj_id: int, session: Sessions, current_user: CurrentUser):
    db_obj = session.scalar(
        select(Projeto).where(
            (Projeto.id_projeto == obj_id) & (Projeto.user_id == current_user.id)
        )
    )
    if not db_obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Projeto not found")
    
    session.delete(db_obj)
    session.commit()
    return {"message": "Projeto deleted"}
