"""
Seed script: inserts 2 sample inversores and 2 sample placas into the database.

Usage:
    poetry run python scripts/seed_equipamentos.py

Requires .env.dev (or .env) with DATABASE_URL set, and the DB running.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv(".env.dev")

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api.schemas.models import Inversor, Placa, table_registry

DATABASE_URL = os.environ["DATABASE_URL"]

INVERSORES = [
    Inversor(
        marca_inversor="DEYE",
        modelo_inversor="SUN-5K-SG03LP1-EU",
        potencia_inversor=5000.0,
        numero_fases="monofasico",
        tipo_de_inversor="string",
        numero_mppt=2,
    ),
    Inversor(
        marca_inversor="GROWATT",
        modelo_inversor="MIN-6000TL-XH",
        potencia_inversor=6000.0,
        numero_fases="monofasico",
        tipo_de_inversor="string",
        numero_mppt=2,
    ),
]

PLACAS = [
    Placa(
        marca_placa="CANADIAN SOLAR",
        modelo_placa="CS6R-410H",
        potencia_placa=410.0,
        tipo_celula="monocrystalino",
        tensao_pico=49.3,
        corrente_curtocircuito=11.09,
        tensao_maxima_potencia=41.8,
        corrente_maxima_potencia=9.82,
        eficiencia_placa=21.4,
    ),
    Placa(
        marca_placa="JINKO SOLAR",
        modelo_placa="JKM415M-54HL4",
        potencia_placa=415.0,
        tipo_celula="monocrystalino",
        tensao_pico=49.5,
        corrente_curtocircuito=10.91,
        tensao_maxima_potencia=41.4,
        corrente_maxima_potencia=10.03,
        eficiencia_placa=20.9,
    ),
]


def seed():
    engine = create_engine(DATABASE_URL)
    with Session(engine) as session:
        for obj in INVERSORES + PLACAS:
            session.add(obj)
        session.commit()
        print(f"Seeded {len(INVERSORES)} inversores and {len(PLACAS)} placas.")


if __name__ == "__main__":
    seed()
