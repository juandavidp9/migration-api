from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from sqlalchemy import text

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
        d.department,
        j.job,
        COUNT(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 1 THEN 1 END) AS Q1,
        COUNT(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 2 THEN 1 END) AS Q2,
        COUNT(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 3 THEN 1 END) AS Q3,
        COUNT(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 4 THEN 1 END) AS Q4
    FROM employees e
    JOIN departments d ON e.department_id = d.id
    JOIN jobs j ON e.job_id = j.id
    WHERE EXTRACT(YEAR FROM e.datetime) = 2021
    GROUP BY d.department, j.job
    ORDER BY d.department, j.job
    """)
    result = db.execute(query)
    return [dict(row) for row in result]

@router.get("/departments-above-mean")
def get_departments_above_mean(db: Session = Depends(get_db)):
    query = text("""
    WITH department_hires AS (
        SELECT 
            d.id,
            d.department,
            COUNT(e.id) as hired
        FROM departments d
        LEFT JOIN employees e ON d.id = e.department_id
        WHERE EXTRACT(YEAR FROM e.datetime) = 2021
        GROUP BY d.id, d.department
    )
    SELECT *
    FROM department_hires
    WHERE hired > (SELECT AVG(hired) FROM department_hires)
    ORDER BY hired DESC
    """)
    result = db.execute(query)
    return [dict(row) for row in result]