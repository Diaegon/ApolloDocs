from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.database import get_session
from api.schemas.models import User
from api.schemas.user import (
    TokenSchema,
)
from api.security import (
    create_access_token,
    verify_password,
)

router = APIRouter(prefix="/token", tags=["Authentication"])
dados_auth = Annotated[OAuth2PasswordRequestForm, Depends()]
Sessions = Annotated[Session, Depends(get_session)]


@router.post("/", response_model=TokenSchema)
def login_for_access_token(
    form_data: dados_auth,
    session: Sessions,
):
    user = session.scalar(select(User).where(User.email == form_data.username))
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
