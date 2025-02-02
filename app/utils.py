from io import StringIO
from . import models 
import csv
from datetime import datetime
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
import os

def parse_csv(file, model, db):
    csv_data = []
    errors = []
    reader = csv.reader(StringIO(file.decode('utf-8')))
    
    for row_number, row in enumerate(reader, start=1):
        # Skip completely empty rows
        if not any(row):
            continue
            
        try:
            # Clean data
            cleaned_row = [val.strip() if isinstance(val, str) else val for val in row]
            cleaned_row = [None if val == '' else val for val in cleaned_row]
            
            # Check if required fields (id and name) are present
            if not cleaned_row[0] or not cleaned_row[1]:
                errors.append(f"Fila {row_number}: ID y nombre son campos requeridos")
                continue
            
            # Create model instance
            data = dict(zip(model.__fields__.keys(), cleaned_row))
            instance = model(**data)
            
            # Only add valid rows
            if instance.name or (model.__name__ != 'EmployeeCreate'):
                csv_data.append(instance)
            else:
                errors.append(f"Fila {row_number}: Registro inválido - nombre vacío")
                
        except Exception as e:
            errors.append(f"Fila {row_number}: {str(e)}")
            
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