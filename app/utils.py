from io import StringIO
from . import models 
import csv
from datetime import datetime
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
import os

import csv
from io import StringIO
from typing import List, Tuple, Any
from pydantic import ValidationError

import csv
from io import StringIO
from typing import List, Tuple, Any
from pydantic import ValidationError

def parse_csv(file: bytes, model: Any, db: Any) -> Tuple[List[Any], List[str]]:
    csv_data = []
    errors = []
    reader = csv.reader(StringIO(file.decode('utf-8')))
    
    for row_number, row in enumerate(reader, start=1):
        if not any(row):
            continue
            
        try:
            cleaned_row = [val.strip() if isinstance(val, str) else val for val in row]
            cleaned_row = [None if val == '' else val for val in cleaned_row]
            
            if model.__name__ == "EmployeeCreate":
                if not cleaned_row[0] or not cleaned_row[1]:
                    errors.append(f"Fila {row_number}: ID y nombre son campos requeridos")
                    continue
            
            data = dict(zip(model.__fields__.keys(), cleaned_row))
            instance = model(**data)
            csv_data.append(instance)
            
        except ValidationError as e:
            errors.append(f"Fila {row_number}: {str(e)}")
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
            detail=f"Error de integridad en la base de datos: {str(e.orig)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado: {str(e)}"
        )