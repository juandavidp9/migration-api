from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas
from app.utils import parse_csv, insert_batch
import os

router = APIRouter()

def process_csv(file, model, db_model, db):
    """
    Procesa un archivo CSV en lotes y lo inserta en la base de datos.
    """
    data, errors = parse_csv(file, model, db)
    
    if errors:
        raise HTTPException(
            status_code=400,
            detail={"message": "Errores de validación en el CSV", "errors": errors}
        )
    
    # Insertar en lotes
    batch_size = int(os.getenv("BATCH_SIZE", 1000))
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        insert_batch(db, batch, db_model)


