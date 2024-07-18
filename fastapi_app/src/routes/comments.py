from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from fastapi_app.src.database import models
from fastapi_app.src import schemas
from fastapi_app.src.repository import comments as crud
from fastapi_app.src.database.db import get_db
from fastapi_app.src.services.auth import auth_service


router = APIRouter()

@router.post("/photos/{photo_id}/comments/", response_model=schemas.Comment)
async def create_comment_for_photo(
    photo_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_service.get_current_user)
):
    return await crud.create_comment(db=db, comment=comment, user_id=current_user.id, photo_id=photo_id)

@router.get("/comments/{comment_id}", response_model=schemas.Comment)
async def read_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = await crud.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

@router.put("/comments/{comment_id}", response_model=schemas.Comment)
async def update_comment(
    comment_id: int,
    comment: schemas.CommentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_service.get_current_user)
):
    db_comment = await crud.get_comment(db, comment_id=comment_id)
    if db_comment is None or db_comment.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Comment not found or not authorized to update")
    return await crud.update_comment(db=db, comment=comment, comment_id=comment_id)

@router.delete("/comments/{comment_id}", response_model=schemas.Comment)
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_service.get_current_user)
):
    db_comment = await crud.get_comment(db, comment_id=comment_id)
    if db_comment is None or current_user.role not in ["admin", "moderator"]:
        raise HTTPException(status_code=404, detail="Comment not found or not authorized to delete")
    return await crud.delete_comment(db=db, comment_id=comment_id)

