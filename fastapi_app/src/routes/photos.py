from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from uuid import uuid4
from fastapi_app.src.database.models import Photo, User
from fastapi_app.src.services.photo_service import PhotoService
from fastapi_app.src.services.auth import auth_service
from fastapi_app.src.database.db import get_db
from fastapi_app.src.repository.tags import create_tags
import aiofiles
import os
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter()

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_photo(file: UploadFile) -> str:
    file_extension = os.path.splitext(file.filename)[1]
    file_name = f"{uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    async with aiofiles.open(file_path, 'wb') as out_file:
        while content := await file.read(1024):
            await out_file.write(content)
    
    return file_path

@router.post("/photos/")
async def create_photo(description: str, tags: Optional[str] = None, file: UploadFile = File(...), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    file_path = await save_photo(file)
    tags = await create_tags([tag for tag in tags.split(' ')])
    photo = Photo(description=description, url=file_path, tags=tags, user_id=current_user.id)
    saved_photo = PhotoService.save(db, photo)
    return saved_photo

@router.put("/photos/{photo_id}")
async def update_photo(photo_id: int, description: str, db: Session = Depends(get_db)):
    try:
        updated_photo = PhotoService.update(db, photo_id, description)
        return updated_photo
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/photos/{photo_id}")
async def delete_photo(photo_id: int, db: Session = Depends(get_db)):
    try:
        PhotoService.delete(db, photo_id)
        return {"detail": "Photo deleted"}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/photos/{photo_id}")
async def read_photo(photo_id: int, db: Session = Depends(get_db)):
    try:
        photo = PhotoService.get(db, photo_id)
        return photo
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))