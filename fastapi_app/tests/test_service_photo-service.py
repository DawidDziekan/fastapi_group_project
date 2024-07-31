import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from fastapi_app.src.services.photo_service import PhotoService
from fastapi_app.src.database.models import Photo

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

def test_save(mock_db):
    photo = Photo(id=1, description="Test photo")
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    saved_photo = PhotoService.save(mock_db, photo)

    mock_db.add.assert_called_once_with(photo)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(photo)
    assert saved_photo == photo

def test_update(mock_db):
    photo = Photo(id=1, description="Test photo")
    mock_db.query().filter().first.return_value = photo
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    updated_photo = PhotoService.update(mock_db, 1, "Updated description")

    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(photo)
    assert updated_photo.description == "Updated description"

def test_update_photo_not_found(mock_db):
    mock_db.query().filter().first.return_value = None

    with pytest.raises(FileNotFoundError):
        PhotoService.update(mock_db, 1, "Updated description")

def test_delete(mock_db):
    photo = Photo(id=1, description="Test photo")
    mock_db.query().filter().first.return_value = photo
    mock_db.delete = MagicMock()
    mock_db.commit = MagicMock()

    PhotoService.delete(mock_db, 1)

    mock_db.delete.assert_called_once_with(photo)
    mock_db.commit.assert_called_once()

def test_delete_photo_not_found(mock_db):
    mock_db.query().filter().first.return_value = None

    with pytest.raises(FileNotFoundError):
        PhotoService.delete(mock_db, 1)

def test_get(mock_db):
    photo = Photo(id=1, description="Test photo")
    mock_db.query().filter().first.return_value = photo

    retrieved_photo = PhotoService.get(mock_db, 1)

    assert retrieved_photo == photo

def test_get_photo_not_found(mock_db):
    mock_db.query().filter().first.return_value = None

    with pytest.raises(FileNotFoundError):
        PhotoService.get(mock_db, 1)
