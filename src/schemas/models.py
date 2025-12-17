from enum import Enum

#Base Enum para outras classes Enum
class BaseEnum(str, Enum):
    def __repr__(self):
        return self.value

class tensao_fase(BaseEnum):
    MONOFASICO = "monofasico"
    BIFASICO = "bifasico"
    TRIFASICO = "trifasico"

class classe_consumo(BaseEnum):
    RESIDENCIAL = "residencial"
    COMERCIAL = "comercial"
    INDUSTRIAL = "industrial"
    RURAL = "rural"

class ramal_de_energia(BaseEnum):
    AEREO = "aereo"
    SUBTERRANEO = "subterraneo"

class tipo_inversor(BaseEnum):
    STRING = "string"
    MICRO = "micro"

class disjuntores(str, Enum):
    A10 = "10 A"
    A16 = "16 A"
    A20 = "20 A"
    A25 = "25 A"
    A32 = "32 A"
    A40 = "40 A"
    A50 = "50 A"
    A63 = "63 A"
    A80 = "80 A"

class cabo_energia(str, Enum):
    MM2_4 = "4 mm²"
    MM2_6 = "6 mm²"
    MM2_10 = "10 mm²"
    MM2_16 = "16 mm²"
    MM2_25 = "25 mm²"
    MM2_35 = "35 mm²"

class corrente_max_cabo(str, Enum):
    cabo_4MM2 = "28 A"
    cabo_6MM2 = "36 A"
    cabo_10MM2 = "50 A"
    cabo_16MM2 = "68 A"
    cabo_25MM2 = "89 A"
    cabo_35MM2 = "111 A"
