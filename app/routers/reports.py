from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from sqlalchemy import text
import logging

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/hires-by-quarter")
def get_hires_by_quarter(db: Session = Depends(get_db)):
    query = text("""
    SELECT 
        d.department as department,
        j.job as job,
        COUNT(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 1 THEN 1 END) AS q1,
        COUNT(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 2 THEN 1 END) AS q2,
        COUNT(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 3 THEN 1 END) AS q3,
        COUNT(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 4 THEN 1 END) AS q4
    FROM employees e
    JOIN departments d ON e.department_id = d.id
    JOIN jobs j ON e.job_id = j.id
    WHERE EXTRACT(YEAR FROM e.datetime) = 2021
    GROUP BY d.department, j.job
    ORDER BY d.department, j.job
    """)
    
    try:
        result = db.execute(query)
        rows = result.fetchall()
        
        if not rows:
            return []
            
        return [
            {
                "department": row.department,
                "job": row.job,
                "q1": row.q1,
                "q2": row.q2,
                "q3": row.q3,
                "q4": row.q4
            }
            for row in rows
        ]
        
    except Exception as e:
        logging.error(f"Error in get_hires_by_quarter: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al ejecutar la consulta: {str(e)}"
        )

@router.get("/departments-above-mean")
def get_departments_above_mean(db: Session = Depends(get_db)):
    query = text("""
    WITH dept_counts AS (
        SELECT 
            d.department,
            COUNT(*) as count,
            AVG(COUNT(*)) OVER () as mean
        FROM employees e
        JOIN departments d ON e.department_id = d.id
        GROUP BY d.department
    )
    SELECT department, count, mean
    FROM dept_counts
    WHERE count > mean
    ORDER BY count DESC
    """)
    
    try:
        result = db.execute(query)
        rows = result.fetchall()
        
        if not rows:
            return []
            
        return [
            {
                "department": row[0],
                "count": row[1],
                "mean": row[2]
            }
            for row in rows
        ]
        
    except Exception as e:
        logging.error(f"Error in get_departments_above_mean: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al ejecutar la consulta: {str(e)}"
        )