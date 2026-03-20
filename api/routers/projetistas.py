from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.database import get_session
from api.schemas.models import Projetista, User
from api.schemas.pageschema import FilterPage
from api.schemas.pessoas.projetista import ProjetistaList, ProjetistaPublic, ProjetistaSchema
from api.security import get_current_user
from api.schemas.user import Message

router = APIRouter(prefix="/projetistas", tags=["Projetistas"])
Sessions = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
filtered_page = Annotated[FilterPage, Query()]

@router.post("/", status_code=HTTPStatus.CREATED, response_model=ProjetistaPublic)
def create_projetista(projetista: ProjetistaSchema, session: Sessions, current_user: CurrentUser):
    db_obj = Projetista(**projetista.model_dump(), user_id=current_user.id)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

@router.get("/", response_model=ProjetistaList)
def read_projetistas(session: Sessions, current_user: CurrentUser, filter_page: filtered_page):
    objs = session.scalars(
        select(Projetista)
        .where(Projetista.user_id == current_user.id)
        .offset(filter_page.offset)
        .limit(filter_page.limit)
    ).unique().all()
    return {"projetistas": objs}

@router.get("/{obj_id}", response_model=ProjetistaPublic)
def read_projetista(obj_id: int, session: Sessions, current_user: CurrentUser):
    db_obj = session.scalar(
        select(Projetista).where(
            (Projetista.id_projetista == obj_id) & (Projetista.user_id == current_user.id)
        )
    )
    if not db_obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Projetista not found")
    return db_obj

@router.put("/{obj_id}", response_model=ProjetistaPublic)
def update_projetista(obj_id: int, projetista: ProjetistaSchema, session: Sessions, current_user: CurrentUser):
    db_obj = session.scalar(
        select(Projetista).where(
            (Projetista.id_projetista == obj_id) & (Projetista.user_id == current_user.id)
        )
    )
    if not db_obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Projetista not found")
    
    for key, value in projetista.model_dump().items():
        setattr(db_obj, key, value)
    
    session.commit()
    session.refresh(db_obj)
    return db_obj

@router.delete("/{obj_id}", response_model=Message)
def delete_projetista(obj_id: int, session: Sessions, current_user: CurrentUser):
    db_obj = session.scalar(
        select(Projetista).where(
            (Projetista.id_projetista == obj_id) & (Projetista.user_id == current_user.id)
        )
    )
    if not db_obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Projetista not found")
    
    session.delete(db_obj)
    session.commit()
    return {"message": "Projetista deleted"}
