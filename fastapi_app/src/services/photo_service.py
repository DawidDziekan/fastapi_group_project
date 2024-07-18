from sqlalchemy.orm import Session
from uuid import UUID
from fastapi_app.src.database.models import Photo
from fastapi_app.src.database.db import SessionLocal

class PhotoService:
    @staticmethod
    def save(photo: Photo) -> Photo:
        db = SessionLocal()
        db.add(photo)
        db.commit()
        db.refresh(photo)
        db.close()
        return photo

    @staticmethod
    def update(photo_id: int, description: str) -> Photo:
        db = SessionLocal()
        photo = db.query(Photo).filter(Photo.id == photo_id).first()
        if photo:
            photo.description = description
            db.commit()
            db.refresh(photo)
        db.close()
        if not photo:
            raise FileNotFoundError(f"Photo with ID {photo_id} not found")
        return photo

    @staticmethod
    def delete(photo_id: int) -> None:
        db = SessionLocal()
        photo = db.query(Photo).filter(Photo.id == photo_id).first()
        if photo:
            db.delete(photo)
            db.commit()
        db.close()
        if not photo:
            raise FileNotFoundError(f"Photo with ID {photo_id} not found")

    @staticmethod
    def get(photo_id: int) -> Photo:
        db = SessionLocal()
        photo = db.query(Photo).filter(Photo.id == photo_id).first()
        db.close()
        if not photo:
            raise FileNotFoundError(f"Photo with ID {photo_id} not found")
        return photo
