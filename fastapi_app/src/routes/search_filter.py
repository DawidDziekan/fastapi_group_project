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
    if not search.keywords and not search.tags:
        raise HTTPException(status_code=400, detail="Keywords or tags must be provided for search")
    return await crud.search_photos(db=db, search=search)

@router.post("/photos/search/user", response_model=List[schemas.Photo])
async def search_photos_by_user(
    search: schemas.UserPhotoSearch,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_service.get_current_user)
):
    if not (current_user.role == "admin" or current_user.role == "moderator"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return await crud.search_photos_by_user(db=db, search=search)
