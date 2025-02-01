from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

class EmployeeCreate(BaseModel):
    id: int
    name: str
    datetime: Optional[datetime]  
    department_id: Optional[int]  
    job_id: Optional[int]  

    @validator("datetime", pre=True)
    def parse_datetime(cls, value):
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("Formato de fecha no válido. Use el formato ISO (YYYY-MM-DDTHH:MM:SSZ).")
        return value

class DepartmentCreate(BaseModel):
    id: int
    department: str

class JobCreate(BaseModel):
    id: int
    job: str