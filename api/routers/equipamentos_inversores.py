from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.database import get_session
from api.schemas.equipamentos.inversor import (
    InversorList,
    InversorPublic,
    InversorSchema,
)
from api.schemas.models import Inversor, User
from api.schemas.pageschema import FilterPage
from api.schemas.user import Message
from api.security import get_current_user

router = APIRouter(prefix="/equipamentos/inversores", tags=["Equipamentos"])
Sessions = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
filtered_page = Annotated[FilterPage, Query()]


@router.post("/", status_code=HTTPStatus.CREATED, response_model=InversorPublic)
def create_inversor(
    inversor: InversorSchema, session: Sessions, current_user: CurrentUser
):
    db_obj = Inversor(**inversor.model_dump())
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


@router.get("/", response_model=InversorList)
def read_inversores(
    session: Sessions,
    current_user: CurrentUser,
    filter_page: filtered_page,
):
    objs = session.scalars(
        select(Inversor).offset(filter_page.offset).limit(filter_page.limit)
    ).all()
    return {"inversores": objs}


@router.get("/{obj_id}", response_model=InversorPublic)
def read_inversor(obj_id: int, session: Sessions, current_user: CurrentUser):
    db_obj = session.scalar(
        select(Inversor).where(Inversor.id_inversor == obj_id)
    )
    if not db_obj:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Inversor not found"
        )
    return db_obj


@router.put("/{obj_id}", response_model=InversorPublic)
def update_inversor(
    obj_id: int,
    inversor: InversorSchema,
    session: Sessions,
    current_user: CurrentUser,
):
    db_obj = session.scalar(
        select(Inversor).where(Inversor.id_inversor == obj_id)
    )
    if not db_obj:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Inversor not found"
        )
    for key, value in inversor.model_dump().items():
        setattr(db_obj, key, value)
    session.commit()
    session.refresh(db_obj)
    return db_obj


@router.delete("/{obj_id}", response_model=Message)
def delete_inversor(obj_id: int, session: Sessions, current_user: CurrentUser):
    db_obj = session.scalar(
        select(Inversor).where(Inversor.id_inversor == obj_id)
    )
    if not db_obj:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Inversor not found"
        )
    session.delete(db_obj)
    session.commit()
    return {"message": "Inversor deleted"}
