class Calculos:
    ### inversor calculos ###
    def get_corrente_saida(self,potencia_inversor, multiplicador, inversor_tensao) -> float:
        """Calcula a corrente de saída do inversor."""
        corrente_saida = potencia_inversor / (multiplicador * inversor_tensao)
        return corrente_saida       

    
    def disjuntor_protecao(self,corrente_saida) -> int:
        """Calcula o disjuntor de proteção do inversor."""
        corrente = corrente_saida
        if corrente <= 10:
            return 10
        elif corrente <= 16:
            return 16
        elif corrente <= 20:
            return 20
        elif corrente <= 25:
            return 25
        elif corrente <= 32:
            return 32
        elif corrente <= 40:
            return 40
        elif corrente <= 50:
            return 50
        elif corrente <= 63:
            return 63
        elif corrente <= 80:
            return 80
        else:
            raise ValueError("Corrente de saída muito alta para disjuntor padrão")

    
    def cabo_energia_inversor(self,corrente_de_saida) -> str:
        """Determina o cabo de energia baseado na corrente de saída."""
        corrente = corrente_de_saida
        if corrente <= 27:
            return "4 mm²"
        elif corrente <= 35:
            return "6 mm²"
        elif corrente <= 49:
            return "10 mm²"
        elif corrente <= 67:
            return "16 mm²"
        elif corrente <= 88:
            return "25 mm²"
        elif corrente <= 110:
            return "35 mm²"
        else:
            raise ValueError("Corrente de saída muito alta para cabo padrão")

    
    def corrente_max_cabo(self,corrente_saida) -> str:
        """Determina a corrente máxima do cabo baseado na corrente de saída."""
        corrente = corrente_saida
        if corrente <= 28:
            return "28 A"
        elif corrente <= 36:
            return "36 A"
        elif corrente <= 50:
            return "50 A"
        elif corrente <= 68:
            return "68 A"
        elif corrente <= 89:
            return "89 A"
        elif corrente <= 111:
            return "111 A"
        else:
            raise ValueError("Corrente de saída muito alta para cabo padrão")

   
    def calculo_queda_tensao(self, corrente_saida, inversor_tensao, cabo_energia_inversor) -> float:
        tensao_queda = round((200 * 0.0173 * 10 * corrente_saida ) / (inversor_tensao * cabo_energia_inversor),2)
        return tensao_queda


    def calculo_potencia_efetiva(self, potencia_total_final):        
        return potencia_total_final * 0.745
    
    def energia_gerada(self, potencia_efetiva):
        return potencia_efetiva * 5.84 * 30 



