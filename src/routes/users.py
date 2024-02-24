from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from ..database.db import get_db
from ..database.models import User
from ..repository import users as repository_users
from ..services.auth import auth_service
from ..conf.config import settings
from ..schemas import UserDb

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve the current user's profile.

    Args:
        current_user (User, optional): Current authenticated user. Defaults to Depends(auth_service.get_current_user).

    Returns:
        UserDb: Details of the current user's profile.
    """
    return current_user


@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    """
    Update the current user's avatar.

    Args:
        file (UploadFile, optional): File containing the new avatar image. Defaults to File(...).
        current_user (User, optional): Current authenticated user. Defaults to Depends(auth_service.get_current_user).
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        UserDb: Updated details of the current user's profile.
    """
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    r = cloudinary.uploader.upload(file.file, public_id=f'contacts/{current_user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'contacts/{current_user.username}')\
                        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user
