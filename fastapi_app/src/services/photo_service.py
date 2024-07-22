from sqlalchemy.orm import Session
from uuid import UUID
from fastapi_app.src.database.models import Photo
from fastapi_app.src.database.db import SessionLocal

    
class PhotoService:
    @staticmethod
    def save(db: Session, photo: Photo) -> Photo:
        db.add(photo)
        db.commit()
        db.refresh(photo)
        return photo

    @staticmethod
    def update(db: Session, photo_id: int, description: str) -> Photo:
        photo = db.query(Photo).filter(Photo.id == photo_id).first()
        if photo:
            photo.description = description
            db.commit()
            db.refresh(photo)
        else:
            raise FileNotFoundError(f"Photo with ID {photo_id} not found")
        return photo

    @staticmethod
    def delete(db: Session, photo_id: int) -> None:
        photo = db.query(Photo).filter(Photo.id == photo_id).first()
        if photo:
            db.delete(photo)
            db.commit()
        else:
            raise FileNotFoundError(f"Photo with ID {photo_id} not found")

    @staticmethod
    def get(db: Session, photo_id: int) -> Photo:
        photo = db.query(Photo).filter(Photo.id == photo_id).first()
        if not photo:
            raise FileNotFoundError(f"Photo with ID {photo_id} not found")
        return photo