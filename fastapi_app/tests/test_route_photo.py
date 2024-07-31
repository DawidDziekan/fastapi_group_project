import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from fastapi import HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from fastapi_app.src.routers.photo_router import create_photo, update_photo, delete_photo, read_photo
from fastapi_app.src.database.models import Photo, User
from fastapi_app.src.services.photo_service import PhotoService
from fastapi_app.src.services.auth import auth_service
from fastapi_app.src.database.db import get_db

# Mock Fixtures
@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

@pytest.fixture
def current_user():
    return User(id=1, email="test@example.com", role="user")

@pytest.fixture
def photo():
    return Photo(id=1, description="Test photo", url="test_path", user_id=1)

# Tests
@pytest.mark.asyncio
async def test_create_photo(mock_db, current_user):
    file = UploadFile(filename="test.jpg", file=MagicMock())
    description = "Test description"
    tags = "tag1 tag2"
    
    with patch("fastapi_app.src.routers.photo_router.save_photo", new=AsyncMock(return_value="test_path")):
        with patch("fastapi_app.src.routers.photo_router.create_tags", new=AsyncMock(return_value=[])):
            with patch("fastapi_app.src.routers.photo_router.auth_service.get_current_user", return_value=current_user):
                saved_photo = await create_photo(description, tags, file, current_user, mock_db)

    assert saved_photo.url == "test_path"
    assert saved_photo.description == description
    assert saved_photo.user_id == current_user.id

@pytest.mark.asyncio
async def test_update_photo(mock_db, photo):
    mock_db.query().filter().first.return_value = photo
    description = "Updated description"

    updated_photo = await update_photo(photo.id, description, mock_db)

    assert updated_photo.description == description
    mock_db.commit.assert_called_once()

@pytest.mark.asyncio
async def test_update_photo_not_found(mock_db):
    mock_db.query().filter().first.return_value = None
    description = "Updated description"

    with pytest.raises(HTTPException) as exc_info:
        await update_photo(1, description, mock_db)
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Photo with ID 1 not found"

@pytest.mark.asyncio
async def test_delete_photo(mock_db, photo):
    mock_db.query().filter().first.return_value = photo

    response = await delete_photo(photo.id, mock_db)

    assert response["detail"] == "Photo deleted"
    mock_db.commit.assert_called_once()

@pytest.mark.asyncio
async def test_delete_photo_not_found(mock_db):
    mock_db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await delete_photo(1, mock_db)
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Photo with ID 1 not found"

@pytest.mark.asyncio
async def test_read_photo(mock_db, photo):
    mock_db.query().filter().first.return_value = photo

    retrieved_photo = await read_photo(photo.id, mock_db)

    assert retrieved_photo == photo

@pytest.mark.asyncio
async def test_read_photo_not_found(mock_db):
    mock_db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await read_photo(1, mock_db)
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Photo with ID 1 not found"
