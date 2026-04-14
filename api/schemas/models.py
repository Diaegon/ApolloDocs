from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column, registry, relationship

from api.schemas.common.enums import tensao_fase, tipo_inversor

table_registry = registry()


@mapped_as_dataclass(table_registry)
class User:
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )


@mapped_as_dataclass(table_registry)
class Cliente:
    __tablename__ = "clientes"

    id_cliente: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome_cliente: Mapped[str]
    cpf: Mapped[str]
    data_nascimento: Mapped[str]
    razao_social: Mapped[str | None]
    nome_fantasia: Mapped[str | None]
    cnpj: Mapped[str | None]
    rg: Mapped[str]
    telefone_cliente: Mapped[str]
    email_cliente: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    enderecos_cliente: Mapped[list["EnderecoCliente"]] = relationship(lazy="joined", init=False)
    enderecos_obra: Mapped[list["EnderecoObra"]] = relationship(lazy="joined", init=False)


@mapped_as_dataclass(table_registry)
class Inversor:
    __tablename__ = "inversores"

    id_inversor: Mapped[int] = mapped_column(init=False, primary_key=True)
    marca_inversor: Mapped[str]
    modelo_inversor: Mapped[str]
    potencia_inversor: Mapped[float]
    numero_fases: Mapped[tensao_fase]
    tipo_de_inversor: Mapped[tipo_inversor | None]
    numero_mppt: Mapped[int | None]
    strings_por_mppt: Mapped[int | None]
    total_strings: Mapped[int | None]


@mapped_as_dataclass(table_registry)
class Placa:
    __tablename__ = "placas"

    id_placa: Mapped[int] = mapped_column(init=False, primary_key=True)
    marca_placa: Mapped[str]
    modelo_placa: Mapped[str]
    potencia_placa: Mapped[float]
    tipo_celula: Mapped[str | None]
    tensao_pico: Mapped[float]
    corrente_curtocircuito: Mapped[float]
    tensao_maxima_potencia: Mapped[float]
    corrente_maxima_potencia: Mapped[float]
    eficiencia_placa: Mapped[float | None]
    rendimento_ano_1: Mapped[float | None]
    rendimento_ano_25: Mapped[float | None]
    peso: Mapped[float | None]
    largura: Mapped[float | None]
    altura: Mapped[float | None]


@mapped_as_dataclass(table_registry)
class Procurador:
    __tablename__ = "procuradores"

    id_procurador: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome_procurador: Mapped[str]
    cpf_procurador: Mapped[str]
    rg_procurador: Mapped[str]
    telefone_procurador: Mapped[str]
    email_procurador: Mapped[str]
    logradouro_procurador: Mapped[str]
    numero_casa_procurador: Mapped[str]
    complemento_procurador: Mapped[str | None]
    cep_procurador: Mapped[str]
    bairro_procurador: Mapped[str]
    cidade_procurador: Mapped[str]
    estado_procurador: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


@mapped_as_dataclass(table_registry)
class Projetista:
    __tablename__ = "projetistas"

    id_projetista: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome_projetista: Mapped[str]
    creci_projetista: Mapped[str]
    rubrica_projetista: Mapped[str]
    telefone_projetista: Mapped[str]
    email_projetista: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


@mapped_as_dataclass(table_registry)
class EnderecoCliente:
    __tablename__ = "enderecocliente"

    id_endereco_cliente: Mapped[int] = mapped_column(init=False, primary_key=True)
    logradouro_cliente: Mapped[str]
    numero_casa_cliente: Mapped[str]
    complemento_casa_cliente: Mapped[str | None]
    cep_cliente: Mapped[str]
    bairro_cliente: Mapped[str]
    cidade_cliente: Mapped[str]
    estado_cliente: Mapped[str]
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id_cliente"))


@mapped_as_dataclass(table_registry)
class EnderecoObra:
    __tablename__ = "enderecoobra"

    id_endereco_obra: Mapped[int] = mapped_column(init=False, primary_key=True)
    logradouro_obra: Mapped[str]
    numero_obra: Mapped[str]
    complemento_obra: Mapped[str | None]
    cep_obra: Mapped[str]
    bairro_obra: Mapped[str]
    cidade_obra: Mapped[str]
    estado_obra: Mapped[str]
    latitude_obra: Mapped[str | None]
    longitude_obra: Mapped[str | None]
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id_cliente"))


@mapped_as_dataclass(table_registry)
class Projeto:
    __tablename__ = "projetos"

    id_projeto: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id_cliente"))
    procurador_id: Mapped[int] = mapped_column(ForeignKey("procuradores.id_procurador"))
    projetista_id: Mapped[int | None] = mapped_column(ForeignKey("projetistas.id_projetista"), default=None)
    inversor_1_id: Mapped[int | None] = mapped_column(ForeignKey("inversores.id_inversor"), default=None)
    inversor_2_id: Mapped[int | None] = mapped_column(ForeignKey("inversores.id_inversor"), default=None)
    inversor_3_id: Mapped[int | None] = mapped_column(ForeignKey("inversores.id_inversor"), default=None)
    placa_1_id: Mapped[int | None] = mapped_column(ForeignKey("placas.id_placa"), default=None)
    placa_2_id: Mapped[int | None] = mapped_column(ForeignKey("placas.id_placa"), default=None)
    placa_3_id: Mapped[int | None] = mapped_column(ForeignKey("placas.id_placa"), default=None)
    cliente: Mapped["Cliente"] = relationship(lazy="joined", init=False)
    procurador: Mapped["Procurador"] = relationship(lazy="joined", init=False)


