import zipfile
from io import BytesIO

from sqlalchemy.orm import Session

from api.schemas.projetos.completo import ProjetoTodos
from api.schemas.projetos.formularioenelce import ProjetoFormularioEnelCe
from api.schemas.projetos.memorial_v2 import ProjetoMemorialV2
from api.schemas.projetos.procuracao import ProjetoProcuracao
from api.schemas.projetos.unifilar_v2 import ProjetoUnifilarV2
from api.services.docs_service import DocsService


class AllDocsService:
    """
    Generates all four project documents from a single ProjetoTodos payload
    and returns them as a ZIP archive.
    """

    @staticmethod
    def _to_memorial_v2(data: ProjetoTodos) -> ProjetoMemorialV2:
        return ProjetoMemorialV2(
            cliente=data.cliente,
            endereco_obra=data.endereco_obra,
            numero_unidade_consumidora=data.numero_unidade_consumidora,
            carga_instalada_kw=data.carga_instalada_kw,
            disjuntor_geral_amperes=data.disjuntor_geral_amperes,
            energia_media_mensal_kwh=data.energia_media_mensal_kwh,
            classe_consumo1=data.classe_consumo,
            tipo_fornecimento=data.tipo_fornecimento,
            ramal_energia=data.ramal_energia,
            data_projeto=data.data_projeto,
            inversores=data.inversores,
            placas=data.placas,
        )

    @staticmethod
    def _to_procuracao(data: ProjetoTodos) -> ProjetoProcuracao:
        return ProjetoProcuracao(
            id_projeto=None,
            cliente=data.cliente,
            endereco_cliente=data.endereco_cliente,
            endereco_obra=data.endereco_obra,
            procurador=data.procurador,
        )

    @staticmethod
    def _to_unifilar_v2(data: ProjetoTodos) -> ProjetoUnifilarV2:
        return ProjetoUnifilarV2(
            nome_projetista=data.nome_projetista,
            cft_crea_projetista=data.cft_crea_projetista,
            nome_cliente=data.cliente.nome_cliente,
            disjuntor_geral_amperes=data.disjuntor_geral_amperes,
            tensao_local=data.tensao_local,
            endereco_obra=data.endereco_obra,
            inversores=data.inversores,
            placas=data.placas,
        )

    @staticmethod
    def _to_formulario(data: ProjetoTodos) -> ProjetoFormularioEnelCe:
        return ProjetoFormularioEnelCe(
            numero_uc=data.numero_unidade_consumidora,
            classe=data.classe_consumo,
            ramal_energia=data.ramal_energia,
            nome_cliente=data.cliente.nome_cliente,
            cpf=data.cliente.cpf,
            telefone_cliente=data.cliente.telefone_cliente,
            email_cliente=data.cliente.email_cliente,
            endereco_obra=data.endereco_obra,
            tensao_local=data.tensao_local,
            carga_instalada_kw=data.carga_instalada_kw,
            potencia_geracao=data.potencia_geracao,
            nome_procurador=data.procurador.nome_procurador,
            cpf_procurador=data.procurador.cpf_procurador,
            email_procurador=data.procurador.email_procurador,
            data_hoje=data.data_projeto,
            telefone_procurador=data.procurador.telefone_procurador,
        )

    @staticmethod
    def generate_all(data: ProjetoTodos, session: Session) -> BytesIO:
        """
        Generates Memorial, Procuração, Diagrama Unifilar and Formulário ENEL-CE
        from a single payload and returns a ZIP BytesIO buffer.
        """
        memorial_buf = DocsService.generate_memorial_v2(
            AllDocsService._to_memorial_v2(data), session
        )
        procuracao_buf = DocsService.generate_procuracao(
            AllDocsService._to_procuracao(data)
        )
        unifilar_buf = DocsService.generate_diagrama_unifilar_v2(
            AllDocsService._to_unifilar_v2(data), session
        )
        formulario_buf = DocsService.generate_formulario_enel(
            AllDocsService._to_formulario(data)
        )

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("memorial_descritivo.pdf", memorial_buf.read())
            zf.writestr("procuracao.pdf", procuracao_buf.read())
            zf.writestr("diagrama_unifilar.pdf", unifilar_buf.read())
            zf.writestr("formulario_enel_ce.pdf", formulario_buf.read())

        zip_buffer.seek(0)
        return zip_buffer
