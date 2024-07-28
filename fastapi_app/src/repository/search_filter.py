from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi_app.src.database.models import Photo
from fastapi_app.src.database import models
from fastapi_app.src import schemas
from datetime import datetime
from fastapi import HTTPException


async def get_description(db: Session, description: str,rating_filter:int = None, created_at: str = None):
    """
    Retrieve one or more photos from the database based on their descriptions.

    :param db: The database session.
    :type db: Session
    :param description: The description to search for (case-insensitive).
    :type description: str
    :return: A list of Photo objects matching the specified description, or an empty list if none found.
    :rtype: List[models.Photo]
    """
    if rating_filter and created_at:
        raise HTTPException(status_code=400, detail="Choose only one filter parameter at once. Rating or created_at")
    
    query = db.query(models.Photo).filter(models.Photo.description.ilike(f'%{description}%')).first()
    print(query)
    if query:
        id = query.id
    if query and rating_filter:
         query2 = db.query(models.Photo).filter(models.Photo.id==id).filter(models.Photo.rating == rating_filter).all()
    elif query and created_at:
        query2 = db.query(models.Photo).filter(models.Photo.id==id).all()
        query2 = [q for q in query2 if str(q.created_at)[0:10] == created_at]
    elif query:
        query2 = db.query(models.Photo).filter(models.Photo.description.ilike(f'%{description}%')).all()              
    else:
        raise HTTPException(status_code=400, detail="description does not exist")
    return query2

async def get_tag(db: Session, tagname: str, rating_filter:int = None, created_at: str = None):
    """
    Retrieve one or more photos from the database based on their tag.

    :param db: The database session.
    :type db: Session
    :param tagname: The tag to search for.
    :type tagname: str
    :return: A list of Photo objects matching the specified tagname.
    :rtype: List[models.Photo]
    """
    if rating_filter and created_at:
        raise HTTPException(status_code=400, detail="Choose only one filter parameter at once. Rating or created_at")
    
    query = db.query(models.Tag).filter(models.Tag.name.ilike(tagname)).first()
    if query:
        id = query.id
    if query and rating_filter:
        query2 = db.query(models.Photo).filter(models.Photo.tags.any(id=id)).filter(models.Photo.rating == rating_filter).all()
    elif query and created_at:
        query2 = db.query(models.Photo).filter(models.Photo.tags.any(id=id)).all()
        query2 = [q for q in query2 if str(q.created_at)[0:10] == created_at]
    elif query:
        query2 = db.query(models.Photo).filter(models.Photo.tags.any(id=id)).all()                  
    else:
        raise HTTPException(status_code=400, detail="Tag does not exist")
    return query2

