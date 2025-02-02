from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    department = Column(String)

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job = Column(String)

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    datetime = Column(DateTime, nullable=True) 
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)  
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=True) 
    department = relationship("Department")
    job = relationship("Job")