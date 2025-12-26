from pydantic import BaseModel, EmailStr


class Projetista(BaseModel):
    id_projetista: int | None = None
    nome_projetista: str = "[NOME DO PROJETISTA]"
    creci_projetista: str = "[CRECI DO PROJETISTA]"
    rubrica_projetista: str = "[RUBRICA DO PROJETISTA]"
    telefone_projetista: str = "[TELEFONE DO PROJETISTA]"
    email_projetista: EmailStr = "email@projeto.br"
