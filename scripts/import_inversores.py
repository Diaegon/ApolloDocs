import csv
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from api.database import engine
from api.schemas.models import Inversor
from api.schemas.common.enums import tensao_fase, tipo_inversor

def run_import():
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../support-files/db inversores'))
    
    inversores_to_add = []
    
    print(f"Reading CSV target: {csv_path}")
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row_idx, row in enumerate(reader, start=2):
            try:
                raw_potencia = row['potencia'].strip()
                if not raw_potencia:
                    continue
                potencia = float(raw_potencia)
                
                fases_str = row['numero_fases'].lower().strip()
                if fases_str not in [e.value for e in tensao_fase]:
                    continue
                
                mppt_val = row['numero_strings'].strip()
                mppt = int(mppt_val) if mppt_val.isdigit() else None
                
                inversor = Inversor(
                    marca_inversor=row['marca'].strip().upper(),
                    modelo_inversor=row['modelo'].strip().upper(),
                    potencia_inversor=potencia,
                    numero_fases=tensao_fase(fases_str),
                    tipo_de_inversor=tipo_inversor.STRING,
                    numero_mppt=mppt
                )
                inversores_to_add.append(inversor)
            except Exception as e:
                print(f"Skipping row {row_idx} due to error: {e}")
                
    if not inversores_to_add:
        print("No valid rows found to import.")
        return

    print(f"Connecting to database to insert {len(inversores_to_add)} records...")
    with Session(engine) as session:
        for inv in inversores_to_add:
            session.add(inv)
        session.commit()
    
    print("Import successfully completed!")

if __name__ == "__main__":
    run_import()
