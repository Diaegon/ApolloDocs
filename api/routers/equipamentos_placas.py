from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.database import get_session
from api.schemas.equipamentos.placa import (
    PlacaList,
    PlacaPublic,
    PlacaSchema,
)
from api.schemas.models import Placa, User
from api.schemas.pageschema import FilterPage
from api.schemas.user import Message
from api.security import get_current_user

router = APIRouter(prefix="/equipamentos/placas", tags=["Equipamentos"])
Sessions = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
filtered_page = Annotated[FilterPage, Query()]


@router.post("/", status_code=HTTPStatus.CREATED, response_model=PlacaPublic)
def create_placa(
    placa: PlacaSchema, session: Sessions, current_user: CurrentUser
):
    db_obj = Placa(**placa.model_dump())
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


@router.get("/", response_model=PlacaList)
def read_placas(
    session: Sessions,
    current_user: CurrentUser,
    filter_page: filtered_page,
):
    objs = session.scalars(
        select(Placa).offset(filter_page.offset).limit(filter_page.limit)
    ).all()
    return {"placas": objs}


@router.get("/{obj_id}", response_model=PlacaPublic)
def read_placa(obj_id: int, session: Sessions, current_user: CurrentUser):
    db_obj = session.scalar(
        select(Placa).where(Placa.id_placa == obj_id)
    )
    if not db_obj:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Placa not found"
        )
    return db_obj


@router.put("/{obj_id}", response_model=PlacaPublic)
def update_placa(
    obj_id: int,
    placa: PlacaSchema,
    session: Sessions,
    current_user: CurrentUser,
):
    db_obj = session.scalar(
        select(Placa).where(Placa.id_placa == obj_id)
    )
    if not db_obj:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Placa not found"
        )
    for key, value in placa.model_dump().items():
        setattr(db_obj, key, value)
    session.commit()
    session.refresh(db_obj)
    return db_obj


@router.delete("/{obj_id}", response_model=Message)
def delete_placa(obj_id: int, session: Sessions, current_user: CurrentUser):
    db_obj = session.scalar(
        select(Placa).where(Placa.id_placa == obj_id)
    )
    if not db_obj:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Placa not found"
        )
    session.delete(db_obj)
    session.commit()
    return {"message": "Placa deleted"}
