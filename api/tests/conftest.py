from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from api.app import app
from api.database import get_session
from api.schemas.models import User, table_registry
from api.security import get_password_hash


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
    engine.dispose()


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 1, 1)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, "created_at"):
            target.created_at = time

    event.listen(model, "before_insert", fake_time_hook)

    yield time

    event.remove(model, "before_insert", fake_time_hook)


@pytest.fixture
def user(session):
    password = "testtest"
    user = User(
        username="Teste",
        email="teste@test.com",
        password=get_password_hash("testtest"),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        "/token",
        data={"username": user.email, "password": user.clean_password},
    )
    return response.json()["access_token"]


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def inversor(session):
    from api.schemas.models import Inversor
    obj = Inversor(
        marca_inversor="DEYE",
        modelo_inversor="SUN-5K-SG03LP1-EU",
        potencia_inversor=5000.0,
        numero_fases="monofasico",
        tipo_de_inversor="string",
        numero_mppt=2,
    )
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


@pytest.fixture
def placa(session):
    from api.schemas.models import Placa
    obj = Placa(
        marca_placa="CANADIAN SOLAR",
        modelo_placa="CS6R-410H",
        potencia_placa=410.0,
        tipo_celula="monocrystalino",
        tensao_pico=49.3,
        corrente_curtocircuito=11.09,
        tensao_maxima_potencia=41.8,
        corrente_maxima_potencia=9.82,
        eficiencia_placa=21.4,
    )
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj
