from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.database import get_session
from api.schemas.models import Procurador, User
from api.schemas.pageschema import FilterPage
from api.schemas.pessoas.procurador import ProcuradorList, ProcuradorPublic, ProcuradorSchema
from api.security import get_current_user
from api.schemas.user import Message

router = APIRouter(prefix="/procuradores", tags=["Procuradores"])
Sessions = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
filtered_page = Annotated[FilterPage, Query()]

@router.post("/", status_code=HTTPStatus.CREATED, response_model=ProcuradorPublic)
def create_procurador(procurador: ProcuradorSchema, session: Sessions, current_user: CurrentUser):
    db_obj = Procurador(**procurador.model_dump(), user_id=current_user.id)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

@router.get("/", response_model=ProcuradorList)
def read_procuradores(session: Sessions, current_user: CurrentUser, filter_page: filtered_page):
    objs = session.scalars(
        select(Procurador)
        .where(Procurador.user_id == current_user.id)
        .offset(filter_page.offset)
        .limit(filter_page.limit)
    ).unique().all()
    return {"procuradores": objs}

@router.get("/{obj_id}", response_model=ProcuradorPublic)
def read_procurador(obj_id: int, session: Sessions, current_user: CurrentUser):
    db_obj = session.scalar(
        select(Procurador).where(
            (Procurador.id_procurador == obj_id) & (Procurador.user_id == current_user.id)
        )
    )
    if not db_obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Procurador not found")
    return db_obj

@router.put("/{obj_id}", response_model=ProcuradorPublic)
def update_procurador(obj_id: int, procurador: ProcuradorSchema, session: Sessions, current_user: CurrentUser):
    db_obj = session.scalar(
        select(Procurador).where(
            (Procurador.id_procurador == obj_id) & (Procurador.user_id == current_user.id)
        )
    )
    if not db_obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Procurador not found")
    
    for key, value in procurador.model_dump().items():
        setattr(db_obj, key, value)
    
    session.commit()
    session.refresh(db_obj)
    return db_obj

@router.delete("/{obj_id}", response_model=Message)
def delete_procurador(obj_id: int, session: Sessions, current_user: CurrentUser):
    db_obj = session.scalar(
        select(Procurador).where(
            (Procurador.id_procurador == obj_id) & (Procurador.user_id == current_user.id)
        )
    )
    if not db_obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Procurador not found")
    
    session.delete(db_obj)
    session.commit()
    return {"message": "Procurador deleted"}
