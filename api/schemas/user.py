from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


# classe de esquema para usuário
class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)
    # created_at: datetime
    # updated_at: datetime | None


class UserList(BaseModel):
    users: list[UserPublic]


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
