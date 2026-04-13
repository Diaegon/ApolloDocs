from http import HTTPStatus
from io import BytesIO

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

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
    def generate_memorial_v2(dados_entrada, session: Session):
        from api.schemas.models import Inversor as InversorORM, Placa as PlacaORM
        from api.schemas.sistema.inversor import Inversor as InversorSchema
        from api.schemas.sistema.materiais import MaterialInversor, MaterialPlaca
        from api.schemas.sistema.placas import Placa as PlacaSchema
        from src.domain.creatememorialobject_v2 import (
            MemorialPresenterV2,
            ObjetosCalculadosV2,
        )
        from src.schemas.modelreturnobject import ProjetoCompletoV2

        inversores = []
        for ref in dados_entrada.inversores:
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

        placas = []
        for ref in dados_entrada.placas:
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
    def generate_procuracao(projeto):
        pdf = Procuracao(projeto)
        pdf.gerar_procuracao()

        buffer = BytesIO(pdf.to_bytes())
        buffer.seek(0)
        return buffer

    @staticmethod
    def generate_diagrama_unifilar_v2(dados_entrada, session: Session):
        from api.schemas.models import Inversor as InversorORM, Placa as PlacaORM
        from api.schemas.sistema.inversor import Inversor as InversorSchema
        from api.schemas.sistema.placas import Placa as PlacaSchema
        from src.domain.creatediagramobject_v2 import (
            ObjetoDiagramaUnifilarV2,
            ProjetoUnifilarResolvido,
            SistemaResolvidoV2,
        )

        sistemas = []
        for ref in dados_entrada.sistemas:
            db_inv = session.scalar(
                select(InversorORM).where(InversorORM.id_inversor == ref.id_inversor)
            )
            if not db_inv:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail=f"Inversor with id {ref.id_inversor} not found",
                )
            db_placa = session.scalar(
                select(PlacaORM).where(PlacaORM.id_placa == ref.id_placa)
            )
            if not db_placa:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail=f"Placa with id {ref.id_placa} not found",
                )
            sistemas.append(
                SistemaResolvidoV2(
                    inversor=InversorSchema.model_validate(db_inv, from_attributes=True),
                    quantidade_inversor=ref.quantidade_inversor,
                    placa=PlacaSchema.model_validate(db_placa, from_attributes=True),
                    quantidade_placas=ref.quantidade_placas,
                )
            )

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
