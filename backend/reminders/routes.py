"""Reminder CRUD API routes."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

try:
    from ..auth.dependencies import get_current_user, get_db
    from ..models.database import Reminder, User
    from ..models.schemas import (
        ReminderCreate,
        ReminderListResponse,
        ReminderResponse,
        ReminderUpdate,
    )
except ImportError:
    from auth.dependencies import get_current_user, get_db
    from models.database import Reminder, User
    from models.schemas import (
        ReminderCreate,
        ReminderListResponse,
        ReminderResponse,
        ReminderUpdate,
    )


router = APIRouter(prefix="/api/reminders", tags=["reminders"])


def _to_response(reminder: Reminder) -> ReminderResponse:
    return ReminderResponse(
        id=reminder.id,
        user_id=reminder.user_id,
        title=reminder.title,
        description=reminder.description,
        reminder_date=reminder.reminder_date.isoformat(),
        related_scheme_name=reminder.related_scheme_name,
        reminder_type=reminder.reminder_type,
        created_at=reminder.created_at.isoformat(),
        updated_at=reminder.updated_at.isoformat(),
    )


@router.post("", response_model=ReminderResponse)
def create_reminder(
    payload: ReminderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ReminderResponse:
    reminder = Reminder(
        user_id=current_user.id,
        title=payload.title.strip(),
        description=payload.description.strip() if payload.description else None,
        reminder_date=payload.reminder_date,
        related_scheme_name=payload.related_scheme_name.strip()
        if payload.related_scheme_name
        else None,
        reminder_type=payload.reminder_type,
    )
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return _to_response(reminder)


@router.get("", response_model=ReminderListResponse)
def list_reminders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ReminderListResponse:
    reminders = (
        db.query(Reminder)
        .filter(Reminder.user_id == current_user.id)
        .order_by(Reminder.reminder_date.asc(), Reminder.id.desc())
        .all()
    )
    return ReminderListResponse(
        reminders=[_to_response(r) for r in reminders],
        total_count=len(reminders),
    )


@router.put("/{reminder_id}", response_model=ReminderResponse)
def update_reminder(
    reminder_id: int,
    payload: ReminderUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ReminderResponse:
    reminder = (
        db.query(Reminder)
        .filter(Reminder.id == reminder_id, Reminder.user_id == current_user.id)
        .first()
    )
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")

    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        if key in {"title", "description", "related_scheme_name"} and isinstance(value, str):
            value = value.strip()
        setattr(reminder, key, value)

    reminder.updated_at = datetime.utcnow()
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return _to_response(reminder)


@router.delete("/{reminder_id}", response_model=dict)
def delete_reminder(
    reminder_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    reminder = (
        db.query(Reminder)
        .filter(Reminder.id == reminder_id, Reminder.user_id == current_user.id)
        .first()
    )
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")

    db.delete(reminder)
    db.commit()
    return {"message": "Reminder deleted", "success": True}
