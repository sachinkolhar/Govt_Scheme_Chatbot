"""Profile photo upload and management routes."""

from datetime import datetime

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

try:
    from ..auth.dependencies import get_current_user, get_db
    from ..models.database import User
    from ..models.schemas import ProfilePhotoResponse
    from ..utils.file_storage import (
        delete_relative_path,
        resolve_relative_path,
        save_profile_photo,
    )
except ImportError:
    from auth.dependencies import get_current_user, get_db
    from models.database import User
    from models.schemas import ProfilePhotoResponse
    from utils.file_storage import delete_relative_path, resolve_relative_path, save_profile_photo


router = APIRouter(prefix="/api/profile/photo", tags=["profile_assets"])


@router.post("", response_model=ProfilePhotoResponse)
def upload_profile_photo(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProfilePhotoResponse:
    delete_relative_path(current_user.profile_photo_path)

    relative_path, _, _ = save_profile_photo(current_user.id, file)
    current_user.profile_photo_path = relative_path
    current_user.profile_photo_updated_at = datetime.utcnow()

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return ProfilePhotoResponse(
        profile_photo_path=current_user.profile_photo_path,
        profile_photo_updated_at=current_user.profile_photo_updated_at.isoformat()
        if current_user.profile_photo_updated_at
        else None,
    )


@router.get("", response_model=ProfilePhotoResponse)
def get_profile_photo(
    current_user: User = Depends(get_current_user),
) -> ProfilePhotoResponse:
    return ProfilePhotoResponse(
        profile_photo_path=current_user.profile_photo_path,
        profile_photo_updated_at=current_user.profile_photo_updated_at.isoformat()
        if current_user.profile_photo_updated_at
        else None,
    )


@router.get("/file")
def get_profile_photo_file(
    current_user: User = Depends(get_current_user),
):
    if not current_user.profile_photo_path:
        return {"message": "Profile photo not set", "success": False}

    file_path = resolve_relative_path(current_user.profile_photo_path)
    return FileResponse(
        path=str(file_path),
        media_type="application/octet-stream",
        filename=file_path.name,
    )


@router.delete("", response_model=ProfilePhotoResponse)
def delete_profile_photo(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProfilePhotoResponse:
    delete_relative_path(current_user.profile_photo_path)

    current_user.profile_photo_path = None
    current_user.profile_photo_updated_at = None
    db.add(current_user)
    db.commit()

    return ProfilePhotoResponse(
        profile_photo_path=None,
        profile_photo_updated_at=None,
    )
