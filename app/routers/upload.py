from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas
from app.utils import parse_csv, insert_batch
import os
from typing import Annotated


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
    
    batch_size = int(os.getenv("BATCH_SIZE", 1000))
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        insert_batch(db, batch, db_model)


@router.post("/upload/departments")
async def upload_departments(
    file: Annotated[UploadFile, File(description="CSV file with departments data")]
):
    """
    Endpoint para cargar departamentos desde un archivo CSV.
    """
    db = SessionLocal()
    try:
        contents = await file.read()
        data, errors = parse_csv(contents, schemas.DepartmentCreate, db)
        
        if errors:
            raise HTTPException(
                status_code=400,
                detail={"message": "Errores de validación en el CSV", "errors": errors}
            )
        
        insert_batch(db, data, models.Department)
        return {"message": f"Se insertaron {len(data)} departamentos exitosamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado: {str(e)}"
        )
    finally:
        db.close()


@router.post("/upload/jobs")
async def upload_jobs(file: UploadFile = File(...)):
    """
    Endpoint para cargar jobs desde un archivo CSV.
    """
    db = SessionLocal()
    try:
        contents = await file.read()
        data, errors = parse_csv(contents, schemas.JobCreate, db)
        
        if errors:
            raise HTTPException(
                status_code=400,
                detail={"message": "Errores de validación en el CSV", "errors": errors}
            )
        
        insert_batch(db, data, models.Job)
        return {"message": f"Se insertaron {len(data)} jobs exitosamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado: {str(e)}"
        )
    finally:
        db.close()



@router.post("/upload/employees")
async def upload_employees(
    background_tasks: BackgroundTasks, 
    file: UploadFile = File(...)
):
    """Endpoint para cargar empleados desde CSV"""
    db = SessionLocal()
    try:
        contents = await file.read()
        data, errors = parse_csv(contents, schemas.EmployeeCreate, db)
        
        if data:
            def process_with_new_session():
                db = SessionLocal()
                try:
                    insert_batch(db, data, models.Employee)
                finally:
                    db.close()

            background_tasks.add_task(process_with_new_session)
            
        return {
            "message": f"Procesando {len(data)} empleados válidos en segundo plano",
            "valid_records": len(data),
            "errors": errors if errors else None
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado: {str(e)}"
        )
    finally:
        db.close()