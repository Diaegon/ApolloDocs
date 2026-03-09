"""Procuração PDF builder — Jinja2 + WeasyPrint implementation.
"""

from datetime import datetime
from io import BytesIO
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from src.domain.texts.text_procuracao import TextoProcuracao

# Path to the templates directory
_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


class Procuracao:
    def __init__(self, projeto):
        self.projeto = projeto
        self.texto = TextoProcuracao(projeto)
        self.data = datetime.now().strftime("%d/%m/%Y")
        self._html: str = ""
        self.buffer = BytesIO()

    def gerar_procuracao(self) -> None:
        """Render the Jinja2 template and write the PDF bytes to self.buffer."""
        context = {
            "dados": self.projeto,
            "texto": self.texto,
            "data": self.data,
        }

        env = Environment(loader=FileSystemLoader(str(_TEMPLATES_DIR)))
        template = env.get_template("procuracao.html")
        self._html = template.render(**context)

        pdf_bytes = HTML(string=self._html).write_pdf()
        self.buffer = BytesIO(pdf_bytes)
        self.buffer.seek(0)

    def to_bytes(self) -> bytes:
        """Return the generated PDF as raw bytes."""
        return self.buffer.getvalue()
