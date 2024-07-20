from typing import List

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from fastapi_app.src.database import models
from fastapi_app.src import schemas
from fastapi_app.src.database.db import get_db
from fastapi_app.src.services.auth import auth_service
from fastapi_app.src.repository import search_filter as crud


router = APIRouter()

@router.post("/photos/search", response_model=List[schemas.Photo])
async def search_photos(
    search: schemas.PhotoSearch,
    db: Session = Depends(get_db)
):
    """
    Search photos based on keywords, tags, rating, or date range.

    Args:
        search (schemas.PhotoSearch): The search criteria.
        db (Session): The database session.

    Returns:
        List[schemas.Photo]: A list of photos matching the search criteria.

    Raises:
        HTTPException: If neither keywords nor tags are provided for the search.
    """
    if not search.keywords and not search.tags:
        raise HTTPException(status_code=400, detail="Keywords or tags must be provided for search")
    return await crud.search_photos(db=db, search=search)

@router.post("/photos/search/user", response_model=List[schemas.Photo])
async def search_photos_by_user(
    search: schemas.UserSearch,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_service.get_current_user)
):
    """
    Search photos by user ID, only accessible to admins and moderators.

    Args:
        search (schemas.UserSearch): The search criteria including the user ID.
        db (Session): The database session.
        current_user (models.User): The current authenticated user.

    Returns:
        List[schemas.Photo]: A list of photos uploaded by the specified user.

    Raises:
        HTTPException: If the current user does not have admin or moderator permissions.
        HTTPException: If the user ID is not provided in the search criteria.
    """
    if not (current_user.role == "admin" or current_user.role == "moderator"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if not search.user_id:
        raise HTTPException(status_code=400, detail="User ID must be provided for search")
    return await crud.search_photos_by_user(db=db, user_id=search.user_id)
