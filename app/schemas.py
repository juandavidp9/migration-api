from pydantic import BaseModel, Field, validator
from typing import Optional
from pydantic.config import ConfigDict

class EmployeeCreate(BaseModel):
    id: int
    name: str
    datetime: Optional[str] = None
    department_id: Optional[int] = None
    job_id: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )

    @classmethod
    @validator('name')
    def validate_name(cls, value):
        if not value or not value.strip():
            raise ValueError('El nombre no puede estar vacío')
        return value.strip()

class DepartmentCreate(BaseModel):
    id: int
    department: str

    model_config = ConfigDict(from_attributes=True)

class JobCreate(BaseModel):
    id: int
    job: str

    model_config = ConfigDict(from_attributes=True)