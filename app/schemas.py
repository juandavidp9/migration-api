from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

class EmployeeCreate(BaseModel):
    id: int
    name: str
    datetime: Optional[str] = None  
    department_id: Optional[int] = None
    job_id: Optional[int] = None

    class Config:
        from_attributes = True

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip()
class DepartmentCreate(BaseModel):
    id: int
    department: str

class JobCreate(BaseModel):
    id: int
    job: str