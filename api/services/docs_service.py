from http import HTTPStatus
from io import BytesIO

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.buildingdocuments.formularioENEL import FormularioEnelCe
from src.buildingdocuments.memorialdescritivo import MemorialDescritivo
from src.buildingdocuments.procuracao import Procuracao
from src.buildingdocuments.unifilar import DiagramaUnifilar


class DocsService:

    # ── Shared DB helpers ─────────────────────────────────────────────────────

    @staticmethod
    def get_inversores_data(entrada, session: Session):
        from api.schemas.models import Inversor as InversorORM
        from api.schemas.sistema.inversor import Inversor as InversorSchema
        from api.schemas.sistema.materiais import MaterialInversor

        inversores = []
        for ref in entrada.inversores:
            db_inv = session.scalar(
                select(InversorORM).where(InversorORM.id_inversor == ref.id_inversor)
            )
            if not db_inv:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail=f"Inversor with id {ref.id_inversor} not found",
                )
            inv_schema = InversorSchema.model_validate(db_inv, from_attributes=True)
            inversores.append(MaterialInversor(inversor=inv_schema, quantidade=ref.quantidade))
        return inversores

    @staticmethod
    def get_placas_data(entrada, session: Session):
        from api.schemas.models import Placa as PlacaORM
        from api.schemas.sistema.materiais import MaterialPlaca
        from api.schemas.sistema.placas import Placa as PlacaSchema

        placas = []
        for ref in entrada.placas:
            db_placa = session.scalar(
                select(PlacaORM).where(PlacaORM.id_placa == ref.id_placa)
            )
            if not db_placa:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail=f"Placa with id {ref.id_placa} not found",
                )
            placa_schema = PlacaSchema.model_validate(db_placa, from_attributes=True)
            placas.append(MaterialPlaca(placa=placa_schema, quantidade=ref.quantidade))
        return placas

    # ── Document generators ───────────────────────────────────────────────────

    @staticmethod
    def generate_memorial_v2(dados_entrada, session: Session):
        from src.domain.creatememorialobject_v2 import (
            MemorialPresenterV2,
            ObjetosCalculadosV2,
        )
        from src.schemas.modelreturnobject import ProjetoCompletoV2

        inversores = DocsService.get_inversores_data(dados_entrada, session)
        placas = DocsService.get_placas_data(dados_entrada, session)

        dados = dados_entrada.model_dump(
            exclude_none=True, exclude={"inversores", "placas", "id_projeto"}
        )
        projeto = ProjetoCompletoV2(**dados, inversores=inversores, placas=placas)

        calc = ObjetosCalculadosV2(projeto).calculate()
        retorno = MemorialPresenterV2(projeto, calc).build()
        pdf = MemorialDescritivo(retorno)
        pdf.gerar_memorial()

        buffer = BytesIO(pdf.to_bytes())
        buffer.seek(0)
        return buffer

    @staticmethod
    def generate_diagrama_unifilar_v2(dados_entrada, session: Session):
        from src.domain.creatediagramobject_v2 import (
            ObjetoDiagramaUnifilarV2,
            ProjetoUnifilarResolvido,
            SistemaResolvidoV2,
        )

        inversores = DocsService.get_inversores_data(dados_entrada, session)
        placas = DocsService.get_placas_data(dados_entrada, session)

        sistemas = [
            SistemaResolvidoV2(
                inversor=inv.inversor,
                quantidade_inversor=inv.quantidade,
                placa=placa.placa,
                quantidade_placas=placa.quantidade,
            )
            for inv, placa in zip(inversores, placas)
        ]

        projeto = ProjetoUnifilarResolvido(
            nome_projetista=dados_entrada.nome_projetista,
            cft_crea_projetista=dados_entrada.cft_crea_projetista,
            nome_cliente=dados_entrada.nome_cliente,
            disjuntor_geral_amperes=dados_entrada.disjuntor_geral_amperes,
            tensao_local=dados_entrada.tensao_local,
            endereco_obra=dados_entrada.endereco_obra,
            sistemas=sistemas,
        )

        retorno = ObjetoDiagramaUnifilarV2(projeto).construir_dados_diagrama()
        pdf = DiagramaUnifilar(retorno)
        pdf.gerar_diagrama()

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
    def generate_formulario_enel(dados):
        pdf = FormularioEnelCe(dados)
        pdf.gerar_formulario()

        buffer = BytesIO(pdf.to_bytes())
        buffer.seek(0)
        return buffer
