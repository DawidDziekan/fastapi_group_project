from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fastapi_app.src.database import models as models
from fastapi_app.src import schemas
from fastapi_app.src.database.db import get_db
from fastapi_app.src.services.auth import auth_service
from fastapi_app.src.repository import search_filter as crud
from datetime import datetime

router = APIRouter(prefix="/search_filter", tags=["search_filter"])

@router.get("/photos/search/{description}", response_model=List[schemas.DescriptionSearch])
async def get_photo_by_description(
    description: str,
    rating_filter: int | None = None,
    created_at: str | None = None,
    db: Session = Depends(get_db)
    ):

    query = await crud.get_description(db, description=description, rating_filter = rating_filter, created_at = created_at)
    
    if not query:
         raise HTTPException(status_code=400, detail="Description does not exist")
    return query


@router.get("/photos/search/tag/{tagname}", response_model=List[schemas.TagSearch])
async def get_photo_by_tag(
    tagname: str,
    rating_filter: int | None = None,
    created_at: str | None = None,
    db: Session = Depends(get_db)
    ):
    query = await crud.get_tag(db, tagname=tagname, rating_filter = rating_filter, created_at = created_at)
    
    if not query:
         raise HTTPException(status_code=400, detail="Tag does not exist")
    return query
