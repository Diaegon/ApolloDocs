from http import HTTPStatus

from fastapi import APIRouter

from api.schemas.user import UserPublic, UserSchema

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    return "ok"
