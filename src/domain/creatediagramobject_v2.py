from dataclasses import dataclass
from datetime import date
from typing import Any

from src.domain.utils.calculos import Calculos
from src.schemas.modelreturnobject import (
    ConfiguracaoSistema,
    QuantidadePlacas,
    RetornoProjetoDiagrama,
)


@dataclass
class SistemaResolvidoV2:
    """A single system with fully resolved equipment specs (from DB).

    inversor / placa use duck-typed attribute access — any object with the
    expected fields works (Pydantic schema or domain dataclass).
    potencia_inversor is in Watts; potencia_placa is in Wp.
    """
    inversor: Any
    quantidade_inversor: int
    placa: Any
    quantidade_placas: int


@dataclass
class ProjetoUnifilarResolvido:
    """Domain-layer input for the v2 diagram builder.

    Built by the service layer after DB lookups; the domain never touches
    the DB or SQLAlchemy.
    """
    nome_projetista: str
    cft_crea_projetista: str
    nome_cliente: str
    disjuntor_geral_amperes: float
    tensao_local: int
    endereco_obra: Any
    sistemas: list


class ObjetoDiagramaUnifilarV2:
    """Builds RetornoProjetoDiagrama from a list-based v2 project input.

    Mirrors ObjetoDiagramaUnifilar but works with a list of SistemaResolvidoV2
    instead of the legacy ConfiguracaoSistema slots (sistema_instalado1/2/3).

    Power units: potencia_inversor in W, potencia_placa in Wp — consistent
    with the equipment catalog (DB values).
    """

    def __init__(self, dados: ProjetoUnifilarResolvido):
        self.dados = dados
        self.quantidade_sistemas = len(dados.sistemas)
        self.potencia_total_inversores = 0.0
        self.potencia_total_placas = 0.0

    # ── Static helpers ────────────────────────────────────────────────────────

    @staticmethod
    def _get_multiplicador(numero_fases: str) -> float:
        return 1.73 if numero_fases == "trifasico" else 1.0

    @staticmethod
    def _get_tensao(numero_fases: str) -> int:
        return 380 if numero_fases == "trifasico" else 220

    # ── Per-system text builders ──────────────────────────────────────────────

    def texto_disjuntorgeral_unifilar(self) -> str:
        if self.dados.tensao_local == 220:
            return (
                f"DISJUNTOR\nMONOFÁSICO\n \n"
                f"{self.dados.disjuntor_geral_amperes} A - 220V"
            )
        return (
            f"DISJUNTOR\nTRIFÁSICO\n \n"
            f"{self.dados.disjuntor_geral_amperes} A - 380/220V"
        )

    def texto_disjuntor_protecao(self, sistema: SistemaResolvidoV2) -> str:
        mult = self._get_multiplicador(sistema.inversor.numero_fases)
        tensao = self._get_tensao(sistema.inversor.numero_fases)
        corrente = Calculos.get_corrente_saida(
            potencia_inversor=sistema.inversor.potencia_inversor
            * sistema.quantidade_inversor,
            multiplicador=mult,
            inversor_tensao=tensao,
        )
        disjuntor = Calculos.disjuntor_protecao(corrente)
        if sistema.inversor.numero_fases == "monofasico":
            return f"DISJUNTOR\nMONOFÁSICO\n{disjuntor} A - 220V"
        return f"DISJUNTOR\nTRIFÁSICO\n{disjuntor} A - 380V"

    def cabo_inversor(self, sistema: SistemaResolvidoV2) -> str:
        mult = self._get_multiplicador(sistema.inversor.numero_fases)
        tensao = self._get_tensao(sistema.inversor.numero_fases)
        corrente = Calculos.get_corrente_saida(
            potencia_inversor=sistema.inversor.potencia_inversor
            * sistema.quantidade_inversor,
            multiplicador=mult,
            inversor_tensao=tensao,
        )
        return Calculos.cabo_energia_inversor(corrente)

    def texto_paineis(self, sistema: SistemaResolvidoV2) -> str:
        qtd = sistema.quantidade_placas
        self.potencia_total_placas += sistema.placa.potencia_placa * qtd
        return (
            f"{qtd}x  {sistema.placa.marca_placa} \n {sistema.placa.modelo_placa}"
        )

    def texto_inversor(self, sistema: SistemaResolvidoV2) -> str:
        inv = sistema.inversor
        qtd = sistema.quantidade_inversor
        potencia_kw = inv.potencia_inversor / 1000
        self.potencia_total_inversores += inv.potencia_inversor * qtd
        return (
            f"{qtd}x {inv.marca_inversor} \n {inv.modelo_inversor} - {potencia_kw} kW"
        )

    # ── ConfiguracaoSistema bridge (used by DiagramaUnifilar PDF builder) ─────

    def _to_configuracao_sistema(
        self, sistema: SistemaResolvidoV2
    ) -> ConfiguracaoSistema:
        return ConfiguracaoSistema(
            inversor=sistema.inversor,
            quantidade_inversor=sistema.quantidade_inversor,
            quantidade_total_placas_do_sistema=QuantidadePlacas(
                quantidade_placas=sistema.quantidade_placas
            ),
            placa=sistema.placa,
        )

    # ── Main builder ──────────────────────────────────────────────────────────

    def construir_dados_diagrama(self) -> RetornoProjetoDiagrama:
        sistemas = self.dados.sistemas

        outputs = [
            {
                "disjuntor": self.texto_disjuntor_protecao(s),
                "paineis": self.texto_paineis(s),
                "cabo": self.cabo_inversor(s),
                "inversor": self.texto_inversor(s),
                "config": self._to_configuracao_sistema(s),
            }
            for s in sistemas
        ]

        def _get(idx: int, key: str):
            return outputs[idx][key] if idx < len(outputs) else None

        return RetornoProjetoDiagrama(
            quantidade_sistemas_instalados=self.quantidade_sistemas,
            endereco_obra=self.dados.endereco_obra,
            nome_projetista=self.dados.nome_projetista,
            cft_crea_projetista=self.dados.cft_crea_projetista,
            nome_cliente=self.dados.nome_cliente,
            tensao_local=self.dados.tensao_local,
            data_hoje=date.today().strftime("%d/%m/%Y"),
            texto_disjuntorgeral_unifilar=self.texto_disjuntorgeral_unifilar(),
            texto_disjuntor_protecao1=_get(0, "disjuntor"),
            texto_paineis1=_get(0, "paineis"),
            cabo_inversor1=_get(0, "cabo"),
            texto_inversor1=_get(0, "inversor"),
            sistema_instalado1=_get(0, "config"),
            texto_disjuntor_protecao2=_get(1, "disjuntor"),
            texto_paineis2=_get(1, "paineis"),
            cabo_inversor2=_get(1, "cabo"),
            texto_inversor2=_get(1, "inversor"),
            sistema_instalado2=_get(1, "config"),
            texto_disjuntor_protecao3=_get(2, "disjuntor"),
            texto_paineis3=_get(2, "paineis"),
            cabo_inversor3=_get(2, "cabo"),
            texto_inversor3=_get(2, "inversor"),
            sistema_instalado3=_get(2, "config"),
            potencia_total_inversores=self.potencia_total_inversores,
            potencia_total_placas=self.potencia_total_placas,
        )
