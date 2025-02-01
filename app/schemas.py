from pydantic import BaseModel
from datetime import datetime

class EmployeeCreate(BaseModel):
    id: int
    name: str
    datetime: datetime
    department_id: int
    job_id: int