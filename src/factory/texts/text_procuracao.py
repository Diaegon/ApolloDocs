
class TextoProcuracao():
    def __init__(self,projeto):
            self.projeto = projeto   
     
    def texto_procuracao(self):
        return f"Por esse instrumento particular de procuração, eu, {self.projeto.cliente.nome_cliente}, brasileiro, portador do CPF {self.projeto.cliente.cpf}, \
        residente e domiciliado na {self.projeto.endereco_cliente.logradouro_cliente} {self.projeto.endereco_cliente.numero_casa_cliente}\
        {self.projeto.endereco_cliente.complemento_casa_cliente}, {self.projeto.endereco_cliente.bairro_cliente}, \
        {self.projeto.endereco_cliente.cidade_cliente} {self.projeto.endereco_cliente.estado_cliente},\
        CEP: {self.projeto.endereco_cliente.cep_cliente}, nomeio e constituo meu bastante procurador o Sr. {self.projeto.procurador.nome_procurador}, brasileiro, portador do \
        CPF {self.projeto.procurador.cpf_procurador}, residente e domiciliado na {self.projeto.procurador.logradouro_procurador}, \
        {self.projeto.procurador.numero_casa_procurador} {self.projeto.procurador.complemento_procurador}, {self.projeto.procurador.bairro_procurador}\
        {self.projeto.procurador.cidade_procurador}, {self.projeto.procurador.estado_procurador}, CEP: {self.projeto.procurador.cep_procurador}, {self.projeto.procurador.telefone_procurador}, \
        a quem confiro amplos poderes para me representar junto a ENEL, com o fim de solicitar a \
        ligação do sistema fotovoltaico, e para assinar todos os documentos necessários para solicitação de acesso e vistoria, durante os próximos <b>3 MESES</b>." 


if __name__ == "__main__":
    from src.factorys.datas.createproject import ProjectFactory
    from src.config import INPUTS_DIR
    import json 
    file = INPUTS_DIR / "input_solar.json"
    inputs = json.loads(file.read_text(encoding="utf-8"))
    
    projeto = ProjectFactory.factory(inputs)
    texto = TextoProcuracao(projeto)
    print(texto.texto_procuracao())
    pass