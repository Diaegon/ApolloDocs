from src.config import (
    COMPRIMENTO_CABO_PADRAO_M,
    DIAS_MES_COMERCIAL,
    FATOR_APROVEITAMENTO_STC,
    HORAS_SOL_PLENO_MEDIA_CE,
    RESISTIVIDADE_COBRE,
)


class Calculos:
    @staticmethod
    def get_corrente_saida(
        potencia_inversor, multiplicador, inversor_tensao
    ) -> float:
        """Calcula a corrente de saída do inversor."""
        corrente_saida = potencia_inversor / (multiplicador * inversor_tensao)
        return corrente_saida

    @staticmethod
    def disjuntor_protecao(corrente_saida: float) -> int:
        """Seleciona o disjuntor padrão imediatamente acima da corrente de saída."""
        DISJUNTORES_PADRAO = (10, 16, 20, 25, 32, 40, 50, 63, 80)
        for disjuntor in DISJUNTORES_PADRAO:
            if corrente_saida <= disjuntor:
                return disjuntor

        raise ValueError("Corrente de saída muito alta para disjuntor padrão")

    @staticmethod
    def cabo_energia_inversor(corrente_de_saida: float) -> str:
        """Determina o cabo de energia baseado na corrente de saída."""
        CABOS_INVERSOR_PADRAO = (
            (27, "4 mm²"),
            (35, "6 mm²"),
            (49, "10 mm²"),
            (67, "16 mm²"),
            (88, "25 mm²"),
            (110, "35 mm²"),
        )
        for limite, cabo in CABOS_INVERSOR_PADRAO:
            if corrente_de_saida <= limite:
                return cabo

        raise ValueError("Corrente de saída muito alta para cabo padrão")

    @staticmethod
    def corrente_max_cabo(corrente_saida: float) -> str:
        """Determina a corrente máxima do cabo baseado na corrente de saída."""
        CORRENTE_MAX_CABO_PADRAO = (
            (28, "28 A"),
            (36, "36 A"),
            (50, "50 A"),
            (68, "68 A"),
            (89, "89 A"),
            (111, "111 A"),
        )
        for limite, corrente_str in CORRENTE_MAX_CABO_PADRAO:
            if corrente_saida <= limite:
                return corrente_str

        raise ValueError("Corrente de saída muito alta para cabo padrão")

    @staticmethod
    def calculo_queda_tensao(
        corrente_saida: float,
        inversor_tensao: float,
        cabo_energia_inversor: float,
    ) -> float:
        """Calcula a queda de tensão percentual no cabo do inversor.

        Fórmula: ΔV% = (2 * ρ * L * I) / (S * V)
        onde:
            ρ = RESISTIVIDADE_COBRE         (resistividade do cobre em Ω·mm²/m)
            L = COMPRIMENTO_CABO_PADRAO_M   (comprimento estimado em metros)
            I = corrente_saida
            S = cabo_energia_inversor       (seção transversal em mm²)
            V = inversor_tensao
        """
        tensao_queda = round(
            (2 * RESISTIVIDADE_COBRE * COMPRIMENTO_CABO_PADRAO_M * corrente_saida)
            / (inversor_tensao * cabo_energia_inversor),
            2,
        )
        return tensao_queda

    @staticmethod
    def calculo_potencia_efetiva(potencia_total_final: float) -> float:
        """Calcula a potência efetiva do gerador fotovoltaico.

        Aplica o FATOR_APROVEITAMENTO_STC (74,5%), que desconta as perdas
        atmosféricas, de temperatura e de rendimento do inversor, conforme
        metodologia da NT-010 Coelce e dados georeferenciados do Ceará.
        """
        return potencia_total_final * FATOR_APROVEITAMENTO_STC

    @staticmethod
    def energia_gerada(potencia_efetiva: float) -> float:
        """Calcula a energia média gerada mensalmente (kWh).

        Fórmula: E = Potência_efetiva × HSP × Dias_mês
            HSP  = HORAS_SOL_PLENO_MEDIA_CE  (5,84 kWh/m²/dia — média do Ceará)
            Dias = DIAS_MES_COMERCIAL         (30 dias, mês comercial)
        """
        return potencia_efetiva * HORAS_SOL_PLENO_MEDIA_CE * DIAS_MES_COMERCIAL
