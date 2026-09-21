"""User document upload and management routes."""

import os
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

try:
    from ..auth.dependencies import get_current_user, get_db
    from ..models.database import User, UserDocument
    from ..models.schemas import (
        DocumentUploadResponse,
        DocumentType,
        UserDocumentListResponse,
        UserDocumentResponse,
    )
    from ..utils.file_storage import (
        delete_relative_path,
        resolve_relative_path,
        save_document_file,
    )
except ImportError:
    from auth.dependencies import get_current_user, get_db
    from models.database import User, UserDocument
    from models.schemas import (
        DocumentUploadResponse,
        DocumentType,
        UserDocumentListResponse,
        UserDocumentResponse,
    )
    from utils.file_storage import delete_relative_path, resolve_relative_path, save_document_file


router = APIRouter(prefix="/api/documents", tags=["documents"])

_ALLOWED_DOCUMENT_TYPES: set[str] = {
    "aadhaar_card",
    "pan_card",
    "income_certificate",
    "caste_certificate",
    "disability_certificate",
    "land_documents",
    "other",
}


def _to_response(document: UserDocument) -> UserDocumentResponse:
    return UserDocumentResponse(
        id=document.id,
        user_id=document.user_id,
        document_type=document.document_type,
        original_name=document.original_name,
        mime_type=document.mime_type,
        file_size=document.file_size,
        relative_path=document.relative_path,
        created_at=document.created_at.isoformat(),
    )


@router.post("", response_model=DocumentUploadResponse)
def upload_document(
    document_type: DocumentType = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> DocumentUploadResponse:
    normalized_type = str(document_type).strip().lower()
    if normalized_type not in _ALLOWED_DOCUMENT_TYPES:
        raise HTTPException(status_code=400, detail="Invalid document type")

    relative_path, mime_type, file_size = save_document_file(current_user.id, file)
    document = UserDocument(
        user_id=current_user.id,
        document_type=normalized_type,
        original_name=file.filename or "document",
        stored_name=Path(relative_path).name,
        mime_type=mime_type,
        file_size=file_size,
        relative_path=relative_path,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return DocumentUploadResponse(
        message="Document uploaded successfully",
        document=_to_response(document),
    )


@router.get("", response_model=UserDocumentListResponse)
def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserDocumentListResponse:
    documents = (
        db.query(UserDocument)
        .filter(UserDocument.user_id == current_user.id)
        .order_by(UserDocument.created_at.desc())
        .all()
    )
    return UserDocumentListResponse(
        documents=[_to_response(d) for d in documents],
        total_count=len(documents),
    )


@router.get("/{document_id}/download")
def download_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    document = (
        db.query(UserDocument)
        .filter(UserDocument.id == document_id, UserDocument.user_id == current_user.id)
        .first()
    )
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    file_path = resolve_relative_path(document.relative_path)
    media_type = document.mime_type or "application/octet-stream"
    return FileResponse(
        path=str(file_path),
        media_type=media_type,
        filename=document.original_name,
    )


@router.delete("/{document_id}", response_model=dict)
def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    document = (
        db.query(UserDocument)
        .filter(UserDocument.id == document_id, UserDocument.user_id == current_user.id)
        .first()
    )
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    delete_relative_path(document.relative_path)
    db.delete(document)
    db.commit()
    return {"message": "Document deleted", "success": True}
