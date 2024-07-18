from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from uuid import uuid4
from fastapi_app.src.database.models import Photo, User
from fastapi_app.src.services.photo_service import PhotoService
from fastapi_app.src.services.auth import auth_service
import aiofiles
import os

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
async def create_photo(description: str, file: UploadFile = File(...)):
    file_path = await save_photo(file)
    photo = Photo(description=description, url=file_path)
    saved_photo = PhotoService.save(photo)
    return saved_photo

@router.put("/photos/{photo_id}")
async def update_photo(photo_id: int, description: str):
    try:
        updated_photo = PhotoService.update(photo_id, description)
        return updated_photo
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/photos/{photo_id}")
async def delete_photo(photo_id: int):
    try:
        PhotoService.delete(photo_id)
        return {"detail": "Photo deleted"}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/photos/{photo_id}")
async def read_photo(photo_id: int):
    try:
        photo = PhotoService.get(photo_id)
        return photo
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
