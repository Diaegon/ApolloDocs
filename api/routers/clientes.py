from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.database import get_session
from api.schemas.models import Cliente, EnderecoCliente, EnderecoObra, User
from api.schemas.pageschema import FilterPage
from api.schemas.cliente.cliente import ClienteList, ClientePublic, ClienteSchema
from api.schemas.cliente.endereco import (
    EnderecoClientePublic, 
    EnderecoClienteSchema, 
    EnderecoObraPublic, 
    EnderecoObraSchema
)
from api.security import get_current_user
from api.schemas.user import Message

router = APIRouter(prefix="/clientes", tags=["Clientes"])
Sessions = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
filtered_page = Annotated[FilterPage, Query()]

def __get_cliente_protected(obj_id: int, session: Session, user_id: int):
    c = session.scalar(select(Cliente).where((Cliente.id_cliente == obj_id) & (Cliente.user_id == user_id)))
    if not c:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Cliente not found")
    return c

@router.post("/", status_code=HTTPStatus.CREATED, response_model=ClientePublic)
def create_cliente(cliente: ClienteSchema, session: Sessions, current_user: CurrentUser):
    db_obj = Cliente(**cliente.model_dump(), user_id=current_user.id)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

@router.get("/", response_model=ClienteList)
def read_clientes(session: Sessions, current_user: CurrentUser, filter_page: filtered_page):
    objs = session.scalars(
        select(Cliente)
        .where(Cliente.user_id == current_user.id)
        .offset(filter_page.offset)
        .limit(filter_page.limit)
    ).unique().all()
    return {"clientes": objs}

@router.get("/{obj_id}", response_model=ClientePublic)
def read_cliente(obj_id: int, session: Sessions, current_user: CurrentUser):
    return __get_cliente_protected(obj_id, session, current_user.id)

@router.put("/{obj_id}", response_model=ClientePublic)
def update_cliente(obj_id: int, cliente: ClienteSchema, session: Sessions, current_user: CurrentUser):
    db_obj = __get_cliente_protected(obj_id, session, current_user.id)
    
    for key, value in cliente.model_dump().items():
        setattr(db_obj, key, value)
    
    session.commit()
    session.refresh(db_obj)
    return db_obj

@router.delete("/{obj_id}", response_model=Message)
def delete_cliente(obj_id: int, session: Sessions, current_user: CurrentUser):
    db_obj = __get_cliente_protected(obj_id, session, current_user.id)
    session.delete(db_obj)
    session.commit()
    return {"message": "Cliente deleted"}

# --- Endereços sub-endpoints ---

@router.post("/{obj_id}/enderecos_cliente", status_code=HTTPStatus.CREATED, response_model=EnderecoClientePublic)
def create_endereco_cliente(obj_id: int, end: EnderecoClienteSchema, session: Sessions, current_user: CurrentUser):
    __get_cliente_protected(obj_id, session, current_user.id)
    db_obj = EnderecoCliente(**end.model_dump(), cliente_id=obj_id)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

@router.post("/{obj_id}/enderecos_obra", status_code=HTTPStatus.CREATED, response_model=EnderecoObraPublic)
def create_endereco_obra(obj_id: int, end: EnderecoObraSchema, session: Sessions, current_user: CurrentUser):
    __get_cliente_protected(obj_id, session, current_user.id)
    db_obj = EnderecoObra(**end.model_dump(), cliente_id=obj_id)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj
