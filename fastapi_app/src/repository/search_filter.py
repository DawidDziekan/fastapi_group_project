from sqlalchemy.orm import Session
from sqlalchemy import or_

from fastapi_app.src.database import models
from fastapi_app.src import schemas


def apply_filters(query, search: schemas.PhotoSearch):
    """
    Apply various filters to the photo query based on search criteria.

    Args:
        query (Session.query): The initial query object.
        search (schemas.PhotoSearch): The search criteria.

    Returns:
        Session.query: The query object with applied filters.
    """
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
    """
    Search photos based on various criteria.

    Args:
        db (Session): The database session.
        search (schemas.PhotoSearch): The search criteria.

    Returns:
        List[models.Photo]: A list of photos matching the search criteria.
    """
    query = db.query(models.Photo)
    query = apply_filters(query, search)
    return query.all()

async def search_photos_by_user(db: Session, user_id: int):
    """
    Search photos by a specific user.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user.

    Returns:
        List[models.Photo]: A list of photos uploaded by the specified user.
    """
    query = db.query(models.Photo).filter(models.Photo.user_id == user_id)
    return query.all()