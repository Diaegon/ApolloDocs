from api.schemas.projetos.memorial import ProjetoMemorial
from src.schemas.modelreturnobject import ConfiguracaoSistema, ProjetoCompleto


# classe que trata os dados de entrada do sistem instalado e monta a estrutura correta para o objeto de domínio
class SistemaInstaladoFactory:
    @staticmethod
    def instanciar_sistema_instalado_do_json(inputs) -> ConfiguracaoSistema:
        dados_sistema = inputs
        qtd_total_placas = dados_sistema.quantidade_total_placas_do_sistema
        # Monta o dicionário de dados
        dados = {
            "inversor": dados_sistema.inversor,
            "quantidade_inversor": dados_sistema.quantidade_inversor,
            "placa": dados_sistema.placa,
            "quantidade_total_placas_do_sistema": qtd_total_placas,
        }

        # Adiciona placa2 se existir
        if qtd_total_placas.quantidade_placas2:
            dados["placa2"] = dados_sistema.placa2
            dados["quantidade_placas2"] = qtd_total_placas.quantidade_placas2

        return ConfiguracaoSistema(**dados)

    @staticmethod
    def build_sistema_instalado_list(
        inputs: ProjetoMemorial,
    ) -> list[ConfiguracaoSistema]:
        DOIS_SISTEMAS = 2
        TRES_SISTEMAS = 3
        sistemas = []
        sistema = SistemaInstaladoFactory.instanciar_sistema_instalado_do_json(
            inputs.sistema_instalado1
        )
        sistemas.append(sistema)
        if (
            inputs.quantidade_sistemas_instalados == DOIS_SISTEMAS
            and inputs.sistema_instalado2
        ):
            sistema2 = (
                SistemaInstaladoFactory.instanciar_sistema_instalado_do_json(
                    inputs.sistema_instalado2
                )
            )
            sistemas.append(sistema2)
        if (
            inputs.quantidade_sistemas_instalados == TRES_SISTEMAS
            and inputs.sistema_instalado3
        ):
            sistema3 = (
                SistemaInstaladoFactory.instanciar_sistema_instalado_do_json(
                    inputs.sistema_instalado3
                )
            )
            sistemas.append(sistema3)

        return sistemas


# Criação do objeto de domínio ProjetoCompleto a partir do json de entrada ProjetoMemorial. aproveitando a factory do sistema instalado.
class ProjectFactory:
    @staticmethod
    def factory(inputs_projeto: ProjetoMemorial) -> ProjetoCompleto:
        sistema_instalado = (
            SistemaInstaladoFactory.build_sistema_instalado_list(
                inputs_projeto
            )
        )
        dados = inputs_projeto.model_dump(
            exclude_none=True,
            exclude={
                "sistema_instalado1",
                "sistema_instalado2",
                "sistema_instalado3",
            },
        )
        dados.pop("id_projeto", None)
        return ProjetoCompleto(**dados, sistema_instalado=sistema_instalado)


