import pytest
from api.schemas.sistema.inversor import Inversor
from api.schemas.sistema.placas import Placa
from api.schemas.sistema.materiais import MaterialInversor, MaterialPlaca
from src.schemas.modelreturnobject import ProjetoCompletoV2, Cliente, EnderecoObra
from src.domain.creatememorialobject_v2 import ObjetosCalculadosV2, MemorialPresenterV2

def _create_mock_projeto(inversores, placas):
    return ProjetoCompletoV2(
        numero_unidade_consumidora="123",
        carga_instalada_kw=10.0,
        disjuntor_geral_amperes=40.0,
        energia_media_mensal_kwh=200.0,
        classe_consumo1="residencial",
        tipo_fornecimento="monofasico",
        ramal_energia="aéreo",
        data_projeto="2024",
        cliente=Cliente(id_cliente=1, nome_cliente="diego", cpf="123", rg="123", telefone_cliente="123", email_cliente="12", data_nascimento="01", razao_social="", nome_fantasia="", cnpj=""),
        endereco_obra=EnderecoObra(logradouro_obra="", numero_obra="", complemento_obra="", cep_obra="", bairro_obra="", cidade_obra="", estado_obra="", latitude_obra="", longitude_obra=""),
        inversores=inversores,
        placas=placas
    )

def test_1_um_inversor_com_10_placas():
    inv = Inversor(id_inversor=1, marca_inversor="Growatt", modelo_inversor="MIN 5000", potencia_inversor=5000.0, numero_mppt=2)
    p1 = Placa(id_placa=1, marca_placa="Canadian", modelo_placa="CS3", potencia_placa=500.0, eficiencia_placa=None)
    
    inversores = [MaterialInversor(inversor=inv, quantidade=1)]
    placas = [MaterialPlaca(placa=p1, quantidade=10)]
    
    projeto = _create_mock_projeto(inversores, placas)
    mem = MemorialPresenterV2(projeto, ObjetosCalculadosV2(projeto).calculate()).build()
    
    assert mem.quantidade_final_placas == 10
    # MPPT +1 offset division strategy applies identically here over 2 strings with remainder 0
    assert mem.quantidade_final_de_placas_por_inversor == [[5, 5]]
    assert mem.potencia_inversores == [5000.0]

def test_2_dois_inversores_com_20_placas():
    inv = Inversor(id_inversor=1, marca_inversor="Growatt", modelo_inversor="MIN 5000", potencia_inversor=5000.0, numero_mppt=2)
    p1 = Placa(id_placa=1, marca_placa="Canadian", modelo_placa="CS3", potencia_placa=500.0, eficiencia_placa=None)
    
    inversores = [MaterialInversor(inversor=inv, quantidade=2)]
    placas = [MaterialPlaca(placa=p1, quantidade=20)]
    
    projeto = _create_mock_projeto(inversores, placas)
    mem = MemorialPresenterV2(projeto, ObjetosCalculadosV2(projeto).calculate()).build()
    
    assert mem.quantidade_final_placas == 20
    assert mem.quantidade_final_de_placas_por_inversor == [[5, 5], [5, 5]]
    assert mem.potencia_inversores == [5000.0]

def test_3_um_inversor_com_placas_mistas():
    inv = Inversor(id_inversor=1, marca_inversor="Growatt", modelo_inversor="MIN 5000", potencia_inversor=5000.0, numero_mppt=2)
    p1 = Placa(id_placa=1, marca_placa="Canadian", modelo_placa="Modelo X", potencia_placa=500.0, eficiencia_placa=None)
    p2 = Placa(id_placa=2, marca_placa="Canadian", modelo_placa="Modelo Y", potencia_placa=550.0, eficiencia_placa=None)
    
    inversores = [MaterialInversor(inversor=inv, quantidade=1)]
    placas = [
        MaterialPlaca(placa=p1, quantidade=20),
        MaterialPlaca(placa=p2, quantidade=10)
    ]
    
    projeto = _create_mock_projeto(inversores, placas)
    mem = MemorialPresenterV2(projeto, ObjetosCalculadosV2(projeto).calculate()).build()
    
    assert mem.quantidade_final_placas == 30
    assert "20  modulos Canadian Modelo X, de 500.0Wp" in mem.texto_placas_memorial
    assert "10 modulos Canadian Modelo Y, de 550.0Wp" in mem.texto_placas_memorial
    # MPPT odd remainder distributions test
    # 30 split by 2 MPPT = 15 each string. Remainder 0.
    assert mem.quantidade_final_de_placas_por_inversor == [[15, 15]]
