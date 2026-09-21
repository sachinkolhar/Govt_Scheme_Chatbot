"""Authentication utility helpers."""

try:
    from ..models.database import User
    from ..models.schemas import UserPublic
except ImportError:
    from models.database import User
    from models.schemas import UserPublic


def to_user_public(user: User) -> UserPublic:
    """Serialize a database user into its public schema."""
    return UserPublic(
        id=user.id,
        username=user.username,
        name=user.name,
        age=user.age,
        gender=user.gender,
        state=user.state,
        occupation=user.occupation,
        income=user.income,
        category=user.category,
        disability=bool(user.disability),
        student_status=bool(user.student_status),
        farmer_status=bool(user.farmer_status),
        profile_photo_path=user.profile_photo_path,
        profile_photo_updated_at=user.profile_photo_updated_at.isoformat()
        if user.profile_photo_updated_at
        else None,
    )
