"""Local file storage helpers for user uploads."""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile

try:
    from ..config.settings import BASE_DIR
except ImportError:
    from config.settings import BASE_DIR


UPLOAD_ROOT = Path(BASE_DIR) / "uploads"
DOCUMENTS_DIR = UPLOAD_ROOT / "documents"
PROFILE_PHOTOS_DIR = UPLOAD_ROOT / "profile_photos"
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

ALLOWED_DOCUMENT_MIME_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
}
ALLOWED_PHOTO_MIME_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
}

_EXTENSION_BY_MIME_TYPE = {
    "application/pdf": ".pdf",
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


def ensure_upload_dirs() -> None:
    """Ensure upload directories exist."""
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    PROFILE_PHOTOS_DIR.mkdir(parents=True, exist_ok=True)


def _assert_allowed_mime(content_type: str | None, allowed: set[str]) -> str:
    if not content_type or content_type.lower() not in allowed:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    return content_type.lower()


def _assert_size(content: bytes) -> None:
    if len(content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")


def _safe_user_dir(base_dir: Path, user_id: int) -> Path:
    target = (base_dir / str(user_id)).resolve()
    base = base_dir.resolve()
    if not str(target).startswith(str(base)):
        raise HTTPException(status_code=400, detail="Invalid storage path")
    target.mkdir(parents=True, exist_ok=True)
    return target


def _stored_filename(content_type: str) -> str:
    ext = _EXTENSION_BY_MIME_TYPE.get(content_type, "")
    return f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{uuid4().hex}{ext}"


def _write_bytes(target_path: Path, content: bytes) -> None:
    with target_path.open("wb") as out_file:
        out_file.write(content)


def save_document_file(user_id: int, upload: UploadFile) -> tuple[str, str, int]:
    """Persist an uploaded document and return relative path, mime type, and size."""
    ensure_upload_dirs()
    content_type = _assert_allowed_mime(upload.content_type, ALLOWED_DOCUMENT_MIME_TYPES)
    content = upload.file.read()
    _assert_size(content)

    user_dir = _safe_user_dir(DOCUMENTS_DIR, user_id)
    filename = _stored_filename(content_type)
    target_path = user_dir / filename
    _write_bytes(target_path, content)

    relative_path = os.path.relpath(target_path, BASE_DIR).replace("\\", "/")
    return relative_path, content_type, len(content)


def save_profile_photo(user_id: int, upload: UploadFile) -> tuple[str, str, int]:
    """Persist an uploaded profile photo and return relative path, mime type, and size."""
    ensure_upload_dirs()
    content_type = _assert_allowed_mime(upload.content_type, ALLOWED_PHOTO_MIME_TYPES)
    content = upload.file.read()
    _assert_size(content)

    user_dir = _safe_user_dir(PROFILE_PHOTOS_DIR, user_id)
    filename = _stored_filename(content_type)
    target_path = user_dir / filename
    _write_bytes(target_path, content)

    relative_path = os.path.relpath(target_path, BASE_DIR).replace("\\", "/")
    return relative_path, content_type, len(content)


def resolve_relative_path(relative_path: str) -> Path:
    """Resolve and validate a stored relative path."""
    full_path = (Path(BASE_DIR) / relative_path).resolve()
    root = Path(BASE_DIR).resolve()
    if not str(full_path).startswith(str(root)):
        raise HTTPException(status_code=400, detail="Invalid file path")
    if not full_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return full_path


def delete_relative_path(relative_path: str | None) -> None:
    """Delete a stored file if present."""
    if not relative_path:
        return
    try:
        file_path = (Path(BASE_DIR) / relative_path).resolve()
        root = Path(BASE_DIR).resolve()
        if str(file_path).startswith(str(root)) and file_path.exists():
            file_path.unlink()
    except OSError:
        return
