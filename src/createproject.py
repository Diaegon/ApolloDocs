from src.schemas.schemas import (ProjetoMemorial)

from src.schemas.modelreturnobject import ProjetoCompleto, ConfiguracaoSistema

#criação das classes de sistema isntalado
class SistemaInstaladoFactory:
    @staticmethod
    def instanciar_sistema_instalado_do_json(inputs) -> ConfiguracaoSistema:
        dados_sistema = inputs
        qtd_total_placas = dados_sistema.quantidade_total_placas_do_sistema
        #o (a) é o número do sistema instalado no json de entrada.
        # Monta o dicionário de dados
        dados = {
            'inversor': dados_sistema.inversor,
            'quantidade_inversor': dados_sistema.quantidade_inversor,
            'placa': dados_sistema.placa,
            'quantidade_total_placas_do_sistema': qtd_total_placas
        }
        
        # Adiciona placa2 se existir
        if qtd_total_placas.quantidade_placas2:
            dados['placa2'] = dados_sistema.placa2
            dados['quantidade_placas2'] = qtd_total_placas.quantidade_placas2

        return ConfiguracaoSistema(**dados)
    
    @staticmethod
    def build_sistema_instalado_list(inputs: ProjetoMemorial) -> list[ConfiguracaoSistema]:
        sistemas = []
        sistema = SistemaInstaladoFactory.instanciar_sistema_instalado_do_json(inputs.sistema_instalado1)
        sistemas.append(sistema)
        if inputs.quantidade_sistemas_instalados == 2 and inputs.sistema_instalado2:
            sistema2 = SistemaInstaladoFactory.instanciar_sistema_instalado_do_json(inputs.sistema_instalado2)
            sistemas.append(sistema2)
        if inputs.quantidade_sistemas_instalados == 3 and inputs.sistema_instalado3:
            sistema3 = SistemaInstaladoFactory.instanciar_sistema_instalado_do_json(inputs.sistema_instalado3)
            sistemas.append(sistema3)

        return sistemas

#Criação da instancia final dos dados iniciais do projeto. 
class ProjectFactory:
    @staticmethod
    def factory(inputs_projeto: ProjetoMemorial) -> ProjetoCompleto:
        sistema_instalado = SistemaInstaladoFactory.build_sistema_instalado_list(inputs_projeto)
        dados = inputs_projeto.model_dump(exclude_none=True)
        return ProjetoCompleto(
            dados,
            sistema_instalado=sistema_instalado)

