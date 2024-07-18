from sqlalchemy.orm import Session

from fastapi_app.src.database import models
from fastapi_app.src import schemas

from datetime import datetime


async def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

async def create_comment(db: Session, comment: schemas.CommentCreate, user_id: int, photo_id: int):
    db_comment = models.Comment(**comment.dict(), user_id=user_id, photo_id=photo_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

async def update_comment(db: Session, comment: schemas.CommentUpdate, comment_id: int):
    db_comment = await get_comment(db, comment_id)
    if db_comment:
        for key, value in comment.dict().items():
            setattr(db_comment, key, value)
        db_comment.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_comment)
    return db_comment

async def delete_comment(db: Session, comment_id: int):
    db_comment = await get_comment(db, comment_id)
    if db_comment:
        db.delete(db_comment)
        db.commit()
    return db_comment
