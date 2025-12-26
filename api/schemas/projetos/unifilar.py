from pydantic import BaseModel

from api.schemas.cliente.endereco import EnderecoObra
from api.schemas.common.enums import quantidade_sistemas
from api.schemas.sistema.configuracao import ConfiguracaoSistema


class ProjetoUnifilar(BaseModel):
    nome_projetista: str = "[NOME DO PROJETISTA]"
    cft_crea_projetista: str = "[CFT ou CREA DO PROJETISTA]"
    nome_cliente: str
    quantidade_sistemas_instalados: quantidade_sistemas

    disjuntor_geral_amperes: float = 40.0
    tensao_local: int

    endereco_obra: EnderecoObra
    sistema_instalado1: ConfiguracaoSistema
    sistema_instalado2: ConfiguracaoSistema | None = None
    sistema_instalado3: ConfiguracaoSistema | None = None
