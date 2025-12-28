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

FORMULARIO_ENELCEARA_MENOR_OU_IGUAL_10K = FORMULARIOS_DIR / "formulario_microgeracaoENEL.pdf"
FORMULARIO_ENELCEARA_MAIOR_10K = FORMULARIOS_DIR / "formulario_microgeracaoENEL10kw.pdf"

