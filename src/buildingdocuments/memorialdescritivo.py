"""Memorial Descritivo PDF builder — Jinja2 + WeasyPrint implementation.

Public API is identical to the previous ReportLab version:
    pdf = MemorialDescritivo(retorno)
    pdf.gerar_memorial()
    bytes_data = pdf.to_bytes()
"""

import base64
from io import BytesIO
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from src.config import IMAGES_DIR
from src.domain.texts.text_memorial import TextoMemorial

matplotlib.use("Agg")  # non-interactive backend — safe in server environments

# Path to the templates directory
_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

# Table of contents entries: (title, page estimate)
_TOC = [
    ("1 – Introdução", 3),
    ("1.1 – Identificação do cliente", 3),
    ("2 – Localização do Gerador Fotovoltaico", 3),
    ("2.1 – Planta de situação do gerador", 3),
    ("3 – Carga Instalada", 4),
    ("3.1 – Cálculo da Demanda Média", 4),
    ("3.2 – Cálculo do Fator de Carga Médio", 4),
    ("4 – Gerador Fotovoltaico", 4),
    ("4.1 – Cálculo da Energia Média Gerada", 5),
    ("5 – Diagramas Básicos", 5),
    ("5.1 – Parametrização do inversor", 5),
    ("6 – Instalação Elétrica", 6),
    ("6.1 – Diagrama Unifilar Geral", 6),
    ("6.2 – Dimensionamento da Proteção", 6),
    ("6.3 – Coordenação entre os Disjuntores", 7),
    ("7 – Sinalização", 8),
    ("8 – Responsável Técnico", 9),
]


def _equation_to_b64(equation: str) -> str:
    """Render a LaTeX equation string to a base64-encoded PNG via matplotlib."""
    buf = BytesIO()
    fig, ax = plt.subplots(figsize=(6, 1))
    ax.text(0.5, 0.5, equation, fontsize=18, ha="center", va="center")
    ax.axis("off")
    fig.savefig(buf, bbox_inches="tight", pad_inches=0.1, dpi=150)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def _image_to_b64(path: str) -> str:
    """Read an image from disk and return its base64 encoding."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


class MemorialDescritivo:
    """Generates the Memorial Descritivo PDF from a RetornoProjetoCompleto DTO."""

    def __init__(self, dados):
        self.dados = dados
        self.texto = TextoMemorial(dados)
        self._html: str = ""
        self.buffer = BytesIO()

    def gerar_memorial(self) -> None:
        """Render the Jinja2 template and write the PDF bytes to self.buffer."""
        # --- Equations → base64 PNG ---
        eq_corrente_list_b64 = [
            _equation_to_b64(eq) for eq in self.dados.equacao3
        ]

        context = {
            "dados": self.dados,
            "texto": self.texto,
            "toc": _TOC,
            # Equations
            "eq_demanda_b64": _equation_to_b64(self.dados.equacao),
            "eq_fator_carga_b64": _equation_to_b64(self.dados.equacao2),
            "eq_corrente_list_b64": eq_corrente_list_b64,
            "eq_queda_tensao_b64": _equation_to_b64(self.dados.equacao4),
            # Images
            "img_diagrama_b64": _image_to_b64(
                f"{IMAGES_DIR}/diagramasolar.png"
            ),
            "img_aviso_b64": _image_to_b64(f"{IMAGES_DIR}/aviso.png"),
            "img_assinatura_b64": _image_to_b64(
                f"{IMAGES_DIR}/ASSINATURA.png"
            ),
        }

        env = Environment(loader=FileSystemLoader(str(_TEMPLATES_DIR)))
        template = env.get_template("memorial.html")
        self._html = template.render(**context)

        pdf_bytes = HTML(string=self._html).write_pdf()
        self.buffer = BytesIO(pdf_bytes)
        self.buffer.seek(0)

    def to_bytes(self) -> bytes:
        """Return the generated PDF as raw bytes."""
        return self.buffer.getvalue()
