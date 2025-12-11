from src.schemas.schemas import (Projeto, Cliente, EnderecoCliente, EnderecoObra,
Inversor, Placa, Projetista, Procurador, ConfiguracaoSistema, ProjetoTeste)

#criação das classes de sistema isntalado
class SistemaInstaladoFactory:
    @staticmethod
    def instanciar_sistema_instalado_do_json(inputs: ConfiguracaoSistema, a: int) -> ConfiguracaoSistema:
        dados_sistema = inputs
        qtd_total_placas = dados_sistema['quantidade_total_placas_do_sistema']
        #o (a) é o número do sistema instalado no json de entrada.
        # Monta o dicionário de dados
        dados = {
            'inversor': Inversor(**dados_sistema['inversor']),
            'quantidade_inversor': dados_sistema['quantidade_inversor'],
            'placa': Placa(**dados_sistema['placa']),
            'quantidade_placas': qtd_total_placas['quantidade_placas'],
            'quantidade_total_placas_do_sistema': qtd_total_placas
        }
        
        # Adiciona placa2 se existir
        if qtd_total_placas.get('quantidade_placas2'):
            dados['placa2'] = Placa(**dados_sistema['placa2'])
            dados['quantidade_placas2'] = qtd_total_placas.get('quantidade_placas2')
        
        return ConfiguracaoSistema(**dados)
    
    @staticmethod
    def build_sistema_instalado_list(inputs: ProjetoTeste, config_sistema: ConfiguracaoSistema) -> list[ConfiguracaoSistema]:
        sistemas = []
        for i in range(1, inputs['quantidade_sistemas_instalados'] + 1):
            sistema = SistemaInstaladoFactory.instanciar_sistema_instalado_do_json(config_sistema, i)
            sistemas.append(sistema)
        return sistemas

#Criação da classe final dos dados iniciais do projeto. 
class ProjectFactory:

    @staticmethod
    def factory(inputs: dict, inputs_projeto: dict, config_sistema: ConfiguracaoSistema) -> Projeto:
        sistema_instalado = SistemaInstaladoFactory.build_sistema_instalado_list(inputs_projeto, config_sistema)
        if inputs:
            cliente = Cliente(**inputs['cliente'])
            endereco_cliente = EnderecoCliente(**inputs['endereco_cliente'])
            endereco_obra = EnderecoObra(**inputs['endereco_obra'])
            projetista = Projetista(**inputs['projetista'])
            procurador = Procurador(**inputs['dados_procurador'])
        else:
            cliente = Cliente()
            endereco_cliente = EnderecoCliente()
            endereco_obra = EnderecoObra()
            projetista = Projetista()
            procurador = Procurador()
        
        return Projeto(
            **inputs_projeto,
            
            cliente=cliente,
            endereco_cliente=endereco_cliente,
            endereco_obra=endereco_obra,
            projetista=projetista,
            procurador=procurador,
            sistema_instalado=sistema_instalado
        )

if __name__ == "__main__":
    import json
    from src.config import INPUTS_DIR

    file = INPUTS_DIR / "input_solar.json"
    file2 = INPUTS_DIR / "input_necessario.json"
    inputs = json.loads(file.read_text(encoding="utf-8"))
    inputs_projeto = json.loads(file2.read_text(encoding="utf-8"))
    projeto = ProjectFactory.factory(inputs, inputs_projeto)
    print(projeto)