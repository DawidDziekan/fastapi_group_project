from sqlalchemy.orm import Session
from sqlalchemy import or_

from fastapi_app.src.database import models
from fastapi_app.src import schemas


def apply_filters(query, search: schemas.PhotoSearch):
    if search.keywords:
        query = query.filter(or_(
            models.Photo.description.ilike(f"%{search.keywords}%"),
            models.Photo.tags.any(models.Tag.name.ilike(f"%{search.keywords}%"))
        ))
    if search.tags:
        query = query.filter(models.Photo.tags.any(models.Tag.name.in_(search.tags)))
    if search.min_rating:
        query = query.filter(models.Photo.rating >= search.min_rating)
    if search.max_rating:
        query = query.filter(models.Photo.rating <= search.max_rating)
    if search.start_date:
        query = query.filter(models.Photo.created_at >= search.start_date)
    if search.end_date:
        query = query.filter(models.Photo.created_at <= search.end_date)
    return query

async def search_photos(db: Session, search: schemas.PhotoSearch):
    query = db.query(models.Photo)
    query = apply_filters(query, search)
    return query.all()

async def search_photos_by_user(db: Session, search: schemas.UserPhotoSearch):
    query = db.query(models.Photo)
    if search.user_id:
        query = query.filter(models.Photo.user_id == search.user_id)
    query = apply_filters(query, search)
    return query.all()