from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUTS_DIR = BASE_DIR / "inputs"
OUTPUTS_DIR = BASE_DIR / "output"
IMAGES_DIR = BASE_DIR / "support-files" / "images"
DIAGRAMAS_DIR = BASE_DIR / "support-files" / "templates_diagramaunifilar"
FORMULARIOS_DIR = BASE_DIR / "support-files" / "templates_formularios"

DIAGRAMA_UNIFILAR_TEMPLATE_1 = DIAGRAMAS_DIR / "diagrama1.pdf"
DIAGRAMA_UNIFILAR_TEMPLATE_2 = DIAGRAMAS_DIR / "diagrama2.pdf"
DIAGRAMA_UNIFILAR_TEMPLATE_3 = DIAGRAMAS_DIR / "diagrama3.pdf"

FORMULARIO_ENELCEARA_MENOR_OU_IGUAL_10K = (
    FORMULARIOS_DIR / "formularioinferior10k.pdf"
)
FORMULARIO_ENELCEARA_MAIOR_10K = FORMULARIOS_DIR / "formulariosuperior10k.pdf"


# ---------------------------------------------------------------------------
# Engineering Constants
# ---------------------------------------------------------------------------

# Fraction of STC (Standard Test Conditions) power available after accounting
# for atmosphere losses, temperature, and inverter efficiency.
# Source: NT-010 Coelce / georeferenced irradiation factor for Ceará region.
FATOR_APROVEITAMENTO_STC: float = 0.745

# Average daily Peak Sun Hours (HSP) for the Ceará region (kWh/m²/day).
# Used to estimate monthly energy generation.
# Source: CRESESB / Atlas Solarimétrico do Brasil.
HORAS_SOL_PLENO_MEDIA_CE: float = 5.84

# Number of days in a commercial month used for energy calculations.
DIAS_MES_COMERCIAL: int = 30

# Electrical resistivity of copper (Ω·mm²/m) at 70 °C.
# Used in voltage drop calculation: ΔV = (2 * ρ * L * I) / (S * V).
RESISTIVIDADE_COBRE: float = 0.0173

# Assumed one-way cable run length in meters for voltage drop calculations.
# This is the default design value used when exact run length is unknown.
COMPRIMENTO_CABO_PADRAO_M: float = 10.0
