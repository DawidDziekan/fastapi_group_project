from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
import cloudinary
import cloudinary.uploader

from fastapi_app.src.database.db import get_db
from fastapi_app.src.database.models import User
from fastapi_app.src.repository import users as repository_users
from fastapi_app.src.services.auth import auth_service
from fastapi_app.src.conf.config import settings
from fastapi_app.src.schemas import UserDb

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieves the current authenticated user's information.

    :param current_user: The current user object.
    :type current_user: User
    :return: The current user's information.
    :rtype: UserDb
    """
    return current_user


@router.patch("/avatar", response_model=UserDb)
async def update_avatar_user(
    file: UploadFile = File(),
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Updates the avatar of the current authenticated user.

    :param file: The uploaded file containing the new avatar.
    :type file: UploadFile
    :param current_user: The current user object.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: The updated user object.
    :rtype: UserDb
    :raises HTTPException: If an error occurs while updating the avatar.
    """
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )

    cloudinary.uploader.upload(
        file.file, public_id=f"NotesApp/{current_user.username}", overwrite=True
    )
    src_url = cloudinary.CloudinaryImage(f"NotesApp/{current_user.username}").build_url(
        width=250, height=250, crop="fill"
    )
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user

# New routes for admins and moderators
@router.get("/all", response_model=List[UserDb])
async def read_all_users(
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieves all users' information (admin access required).

    :param current_user: The current user object.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: A list of all users.
    :rtype: List[UserDb]
    :raises HTTPException: If the current user does not have admin privileges.
    """
    await auth_service.check_role(current_user, "admin")
    users = db.query(User).all()
    return users


@router.delete("/{user_id}", response_model=dict)
async def delete_user(
    user_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deletes a user by their ID (admin access required).

    :param user_id: The ID of the user to be deleted.
    :type user_id: int
    :param current_user: The current user object.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: A message indicating the result of the deletion.
    :rtype: dict
    :raises HTTPException: If the user is not found or if the current user does not have admin privileges.
    """
    await auth_service.check_role(current_user, "admin")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}


@router.patch("/{user_id}/role", response_model=UserDb)
async def update_user_role(
    user_id: int,
    role: str,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Updates the role of a user (admin access required).

    :param user_id: The ID of the user whose role is to be updated.
    :type user_id: int
    :param role: The new role to assign to the user.
    :type role: str
    :param current_user: The current user object.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: The updated user object.
    :rtype: UserDb
    :raises HTTPException: If the user is not found or if the current user does not have admin privileges.
    """
    await auth_service.check_role(current_user, "admin")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if role not in ["user", "moderator"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    user.role = role
    db.commit()
    db.refresh(user)
    return user
