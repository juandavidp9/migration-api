import pytest
from fastapi.testclient import TestClient
from fastapi import UploadFile, BackgroundTasks
from app.main import app
from app.database import Base, engine, SessionLocal
import io
from app.routers.upload import upload_employees

# Fixtures
@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    client = TestClient(app)
    yield client
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Tests
class TestEmployeeUpload:
    @pytest.mark.asyncio
    async def test_empty_csv_upload(self, mocker):
        """Test con CSV vacío"""
        # Arrange
        mock_file = mocker.AsyncMock(spec=UploadFile)
        mock_file.read.return_value = b""
        mock_file.filename = "test.csv"
        
        mock_db = mocker.MagicMock()
        mocker.patch('app.routers.upload.SessionLocal', return_value=mock_db)
        
        background_tasks = BackgroundTasks()
        
        # Act
        response = await upload_employees(background_tasks, mock_file)
        
        # Assert
        assert isinstance(response, dict)
        assert response["valid_records"] == 0
        assert "Procesando 0 empleados" in response["message"]
        mock_db.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_valid_csv_upload(self, mocker):
        """Test con CSV válido"""
        # Arrange
        csv_content = b"id,name,datetime,department_id,job_id\n1,Test User,2024-01-01,1,1"
        mock_file = mocker.AsyncMock(spec=UploadFile)
        mock_file.read.return_value = csv_content
        mock_file.filename = "test.csv"
        
        mock_db = mocker.MagicMock()
        mocker.patch('app.routers.upload.SessionLocal', return_value=mock_db)
        
        background_tasks = BackgroundTasks()
        
        # Act
        response = await upload_employees(background_tasks, mock_file)
        
        # Assert
        assert response["valid_records"] > 0
        assert "Procesando" in response["message"]
        assert len(background_tasks.tasks) == 1