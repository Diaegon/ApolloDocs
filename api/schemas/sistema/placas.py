from pydantic import BaseModel


class Placa(BaseModel):
    id_placa: int | None
    marca_placa: str = "[MARCA DA PLACA]"
    modelo_placa: str = "[MODELO DA PLACA]"
    potencia_placa: float = 0.0
    tipo_celula: str = "[TIPO DE CÉLULA DA PLACA]"
    tensao_pico: float = 0.0
    corrente_curtocircuito: float = 0.0
    tensao_maxima_potencia: float = 0.0
    corrente_maxima_potencia: float = 0.0
    eficiencia_placa: float | None  # reservado para atualizações futuras

class Placa_v2(BaseModel):
    marca_placa: str
    modelo_placa: str
    quantidade: int
