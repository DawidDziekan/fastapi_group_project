import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi_app.src.routers.search_filter import get_photo_by_description, get_photo_by_tag
from fastapi_app.src.schemas import DescriptionSearch, TagSearch

# Mock Fixtures
@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

# Tests for get_photo_by_description
@pytest.mark.asyncio
async def test_get_photo_by_description(mock_db):
    description = "Test description"
    rating_filter = 5
    created_at = "2023-01-01"

    mock_result = [DescriptionSearch(description="Test description", url="test_url", rating=5, created_at="2023-01-01")]
    with patch("fastapi_app.src.routers.search_filter.crud.get_description", new=AsyncMock(return_value=mock_result)):
        result = await get_photo_by_description(description, rating_filter, created_at, mock_db)
    
    assert result == mock_result

@pytest.mark.asyncio
async def test_get_photo_by_description_not_found(mock_db):
    description = "Non-existing description"
    
    with patch("fastapi_app.src.routers.search_filter.crud.get_description", new=AsyncMock(return_value=None)):
        with pytest.raises(HTTPException) as exc_info:
            await get_photo_by_description(description, None, None, mock_db)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Description does not exist"

# Tests for get_photo_by_tag
@pytest.mark.asyncio
async def test_get_photo_by_tag(mock_db):
    tagname = "Test tag"
    rating_filter = 5
    created_at = "2023-01-01"

    mock_result = [TagSearch(tagname="Test tag", url="test_url", rating=5, created_at="2023-01-01")]
    with patch("fastapi_app.src.routers.search_filter.crud.get_tag", new=AsyncMock(return_value=mock_result)):
        result = await get_photo_by_tag(tagname, rating_filter, created_at, mock_db)
    
    assert result == mock_result

@pytest.mark.asyncio
async def test_get_photo_by_tag_not_found(mock_db):
    tagname = "Non-existing tag"
    
    with patch("fastapi_app.src.routers.search_filter.crud.get_tag", new=AsyncMock(return_value=None)):
        with pytest.raises(HTTPException) as exc_info:
            await get_photo_by_tag(tagname, None, None, mock_db)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Tag does not exist"
