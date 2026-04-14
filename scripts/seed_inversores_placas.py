"""
Seed script: insert inversores and placas from CSV files into the database.
Run from the project root:
    python scripts/seed_inversores_placas.py
"""
import csv
import os
import sys

from dotenv import load_dotenv
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

load_dotenv(".env.dev")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.schemas.common.enums import tensao_fase, tipo_inversor
from api.schemas.models import Inversor, Placa, table_registry

DATABASE_URL = os.environ["DATABASE_URL"]

PHASE_MAP = {
    "single-phase": tensao_fase.MONOFASICO,
    "three-phase": tensao_fase.TRIFASICO,
    "monofasico": tensao_fase.MONOFASICO,
    "bifasico": tensao_fase.BIFASICO,
    "trifasico": tensao_fase.TRIFASICO,
}

TYPE_MAP = {
    "string": tipo_inversor.STRING,
    "microinversor": tipo_inversor.MICRO,
    "string-hybrid": tipo_inversor.STRING_HYBRID,
}


def parse_float(value: str) -> float | None:
    value = value.strip().replace(",", ".")
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def parse_int(value: str) -> int | None:
    value = value.strip()
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def seed_inversores(session: Session) -> int:
    path = "inversors datasheet.csv"
    skipped = []
    inserted = 0

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            phase_raw = row["phase"].strip()
            type_raw = row["inverter_type"].strip()

            if phase_raw not in PHASE_MAP:
                skipped.append(
                    f"  SKIP (bad phase='{phase_raw}'): {row['brand']} {row['model']}"
                )
                continue

            inv = Inversor(
                marca_inversor=row["brand"].strip(),
                modelo_inversor=row["model"].strip(),
                potencia_inversor=float(row["power_kw"].replace(",", ".")),
                numero_fases=PHASE_MAP[phase_raw],
                tipo_de_inversor=TYPE_MAP.get(type_raw),
                numero_mppt=parse_int(row["mppt_number"]),
                strings_por_mppt=parse_int(row["strings_per_mppt"]),
                total_strings=parse_int(row["total_strings"]),
            )
            session.add(inv)
            inserted += 1

    if skipped:
        print("Inversores skipped:")
        for s in skipped:
            print(s)

    return inserted


def seed_placas(session: Session) -> int:
    path = "placas datasheet.csv"
    seen = set()
    inserted = 0

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            marca = row["marca "].strip()
            modelo = row["modelo "].strip()
            key = (marca, modelo)

            if key in seen:
                continue
            seen.add(key)

            placa = Placa(
                marca_placa=marca,
                modelo_placa=modelo,
                potencia_placa=float(row["potencia "].strip()),
                tipo_celula=None,
                tensao_pico=parse_float(row["tensao_circuito_aberto"]),
                corrente_curtocircuito=parse_float(row["corrente_curto_circuito"]),
                tensao_maxima_potencia=parse_float(row["tensao_maxima_potencia"]),
                corrente_maxima_potencia=parse_float(row["corrente_maxima_potencia"]),
                eficiencia_placa=parse_float(row["eficiencia"]),
                rendimento_ano_1=parse_float(row["rendimento_ano_1"]),
                rendimento_ano_25=parse_float(row["rendimento_ano_25"]),
                peso=parse_float(row["peso"]),
                largura=parse_float(row["largura"]),
                altura=parse_float(row["altura"]),
            )
            session.add(placa)
            inserted += 1

    return inserted


def main():
    engine = create_engine(DATABASE_URL)

    with Session(engine) as session:
        print("Clearing existing data...")
        session.execute(
            sa.text(
                "UPDATE projetos SET inversor_1_id=NULL, inversor_2_id=NULL, "
                "inversor_3_id=NULL, placa_1_id=NULL, placa_2_id=NULL, placa_3_id=NULL"
            )
        )
        session.execute(sa.text("DELETE FROM inversores"))
        session.execute(sa.text("DELETE FROM placas"))

        print("Seeding inversores...")
        n_inv = seed_inversores(session)

        print("Seeding placas...")
        n_pla = seed_placas(session)

        session.commit()

    print(f"\nDone. Inserted {n_inv} inversores, {n_pla} placas.")


if __name__ == "__main__":
    main()
