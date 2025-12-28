from datetime import datetime

from pydantic import BaseModel, EmailStr


# classe de esquema para usuário
class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime | None


class TokenSchema(BaseModel):
    access_token: str
    token_type: str

class UserDB(UserSchema):
    id: int