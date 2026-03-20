from pydantic import BaseModel, ConfigDict, EmailStr


class ProjetistaSchema(BaseModel):
    nome_projetista: str = "[NOME DO PROJETISTA]"
    creci_projetista: str = "[CRECI DO PROJETISTA]"
    rubrica_projetista: str = "[RUBRICA DO PROJETISTA]"
    telefone_projetista: str = "[TELEFONE DO PROJETISTA]"
    email_projetista: EmailStr = "email@projeto.br"

class ProjetistaPublic(ProjetistaSchema):
    id_projetista: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)

class ProjetistaList(BaseModel):
    projetistas: list[ProjetistaPublic]

Projetista = ProjetistaSchema
