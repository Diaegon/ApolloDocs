from io import BytesIO

from src.buildingdocuments.formularioENEL import FormularioEnelCe
from src.buildingdocuments.memorialdescritivo import MemorialDescritivo
from src.buildingdocuments.procuracao import Procuracao
from src.buildingdocuments.unifilar import DiagramaUnifilar
from src.createproject import ProjectFactory
from src.domain.creatediagramobject import ObjetoDiagramaUnifilar
from src.domain.creatememorialobject import ObjetosCalculados


class DocsService:
    @staticmethod
    def generate_memorial(dados_entrada):
        projeto = ProjectFactory.factory(dados_entrada)
        retorno = ObjetosCalculados(projeto).calculate().construtor_dados_memorial()
        pdf = MemorialDescritivo(retorno)
        pdf.gerar_memorial()

        buffer = BytesIO(pdf.to_bytes())
        buffer.seek(0)
        return buffer

    @staticmethod
    def generate_procuracao(projeto):
        pdf = Procuracao(projeto)
        pdf.gerar_procuracao()

        buffer = BytesIO(pdf.to_bytes())
        buffer.seek(0)
        return buffer

    @staticmethod
    def generate_diagrama_unifilar(dados):
        projeto = ObjetoDiagramaUnifilar(dados).construir_dados_diagrama()
        pdf = DiagramaUnifilar(projeto)
        pdf.gerar_diagrama()

        buffer = BytesIO(pdf.to_bytes())
        buffer.seek(0)
        return buffer

    @staticmethod
    def generate_formulario_enel(dados):
        pdf = FormularioEnelCe(dados)
        pdf.gerar_formulario()

        buffer = BytesIO(pdf.to_bytes())
        buffer.seek(0)
        return buffer
