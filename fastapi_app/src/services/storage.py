import aiofiles
import os
from uuid import uuid4, UUID
from fastapi import UploadFile

from fastapi_app.src.database.models import Photo

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

async def delete_photo(photo_id: UUID):
    photo = Photo.get(photo_id)
    if not photo:
        raise FileNotFoundError("Photo not found")
    
    file_path = photo.file_path
    if os.path.exists(file_path):
        os.remove(file_path)
    Photo.delete(photo_id)

async def update_photo_description(photo_id: UUID, description: str):
    photo = Photo.get(photo_id)
    if not photo:
        raise FileNotFoundError("Photo not found")
    
    Photo.update(photo_id, description)

async def get_photo(photo_id: UUID) -> str:
    photo = Photo.get(photo_id)
    if not photo:
        raise FileNotFoundError("Photo not found")
    
    return photo.file_path
