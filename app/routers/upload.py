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


@router.post("/upload/employees")
async def upload_employees(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Endpoint para cargar empleados desde un archivo CSV.
    """
    db = SessionLocal()
    try:
        contents = await file.read()
        
        # Procesar el CSV en segundo plano
        background_tasks.add_task(process_csv, contents, schemas.EmployeeCreate, models.Employee, db)
        
        return {"message": "CSV recibido y en proceso de inserción"}
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado: {str(e)}"
        )
    finally:
        db.close()