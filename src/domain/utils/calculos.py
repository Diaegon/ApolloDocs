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
        DISJUNTORES_PADRAO = (10, 16, 20, 25, 32, 40, 50, 63, 80)
        for disjuntor in DISJUNTORES_PADRAO:
            if corrente_saida <= disjuntor:
                return disjuntor

        raise ValueError("Corrente de saída muito alta para disjuntor padrão")

    @staticmethod
    def cabo_energia_inversor(corrente_de_saida: float) -> str:
        CABOS_INVERSOR_PADRAO = (
            (27, "4 mm²"),
            (35, "6 mm²"),
            (49, "10 mm²"),
            (67, "16 mm²"),
            (88, "25 mm²"),
            (110, "35 mm²"),
        )
        """Determina o cabo de energia baseado na corrente de saída."""
        for limite, cabo in CABOS_INVERSOR_PADRAO:
            if corrente_de_saida <= limite:
                return cabo

        raise ValueError("Corrente de saída muito alta para cabo padrão")

    @staticmethod
    def corrente_max_cabo(corrente_saida: float) -> str:
        CORRENTE_MAX_CABO_PADRAO = (
            (28, "28 A"),
            (36, "36 A"),
            (50, "50 A"),
            (68, "68 A"),
            (89, "89 A"),
            (111, "111 A"),
        )
        """Determina a corrente máxima do cabo baseado na corrente de saída."""
        for limite, corrente_str in CORRENTE_MAX_CABO_PADRAO:
            if corrente_saida <= limite:
                return corrente_str

        raise ValueError("Corrente de saída muito alta para cabo padrão")

    @staticmethod
    def calculo_queda_tensao(
        corrente_saida, inversor_tensao, cabo_energia_inversor
    ) -> float:
        tensao_queda = round(
            (200 * 0.0173 * 10 * corrente_saida)
            / (inversor_tensao * cabo_energia_inversor),
            2,
        )
        return tensao_queda

    @staticmethod
    def calculo_potencia_efetiva(potencia_total_final):
        return potencia_total_final * 0.745

    @staticmethod
    def energia_gerada(potencia_efetiva):
        return potencia_efetiva * 5.84 * 30
