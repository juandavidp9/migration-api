from io import StringIO
import csv
from datetime import datetime
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
import os

def parse_csv(file, model, db):
    """
    Parsea un archivo CSV y valida cada fila según el modelo Pydantic.
    Retorna una lista de objetos válidos y una lista de errores.
    """
    csv_data = []
    errors = []
    reader = csv.reader(StringIO(file.decode('utf-8')))
    
    for row_number, row in enumerate(reader, start=1):
        if len(row) != len(model.__fields__):
            errors.append(f"Fila {row_number}: Número incorrecto de columnas. Se esperaban {len(model.__fields__)}, se encontraron {len(row)}")
            continue
        
        try:
            # Convertir y validar la fila usando el modelo Pydantic
            if model.__name__ == "EmployeeCreate":

                # Validar que department_id y job_id existan en la base de datos
                department_id = int(row[3]) if row[3] else None
                job_id = int(row[4]) if row[4] else None

                if department_id and not db.query(models.Department).filter(models.Department.id == department_id).first():
                    errors.append(f"Fila {row_number}: department_id {department_id} no existe en la base de datos.")
                    continue

                if job_id and not db.query(models.Job).filter(models.Job.id == job_id).first():
                    errors.append(f"Fila {row_number}: job_id {job_id} no existe en la base de datos.")
                    continue

                row[2] = datetime.fromisoformat(row[2]) if row[2] else None

            csv_data.append(model(**dict(zip(model.__fields__.keys(), row))))
        except ValidationError as e:
            errors.append(f"Fila {row_number}: Error de validación - {str(e)}")
        except ValueError as e:
            errors.append(f"Fila {row_number}: Error de valor - {str(e)}")
    
    return csv_data, errors



def insert_batch(db, data, db_model):
    """
    Inserta un lote de datos en la base de datos.
    Maneja errores de integridad y realiza commit por lote.
    """
    try:
        db.bulk_insert_mappings(db_model, [item.dict() for item in data])
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error de integridad en la base de datos: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado al insertar datos: {str(e)}"
        )