from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from pydantic.config import ConfigDict

class EmployeeCreate(BaseModel):
    id: int
    name: str
    datetime: Optional[str] = None
    department_id: Optional[int] = None
    job_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip()

class DepartmentCreate(BaseModel):
    id: int
    department: str

    model_config = ConfigDict(from_attributes=True)

class JobCreate(BaseModel):
    id: int
    job: str

    model_config = ConfigDict(from_attributes=True)