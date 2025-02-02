from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

class EmployeeCreate(BaseModel):
    id: int
    name: Optional[str] = None
    datetime: Optional[datetime] = None
    department_id: Optional[int] = None
    job_id: Optional[int] = None

    @validator('name')
    def validate_name(cls, v):
        if v and v.strip():
            return v.strip()
        return None

class DepartmentCreate(BaseModel):
    id: int
    department: str

class JobCreate(BaseModel):
    id: int
    job: str