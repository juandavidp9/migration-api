from sqlalchemy import create_engine
from fastapi import FastAPI
from app.routers import upload, reports
from app.database import engine, Base
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(upload.router, prefix="/api/v1")
app.include_router(reports.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "CSV Migration API"}