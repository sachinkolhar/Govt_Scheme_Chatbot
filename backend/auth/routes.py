"""Authentication API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

try:
    from ..auth.dependencies import get_current_user, get_db
    from ..auth.security import create_access_token, hash_password, verify_password
    from ..auth.utils import to_user_public
    from ..models.database import User
    from ..models.schemas import (
        TokenResponse,
        UserLogin,
        UserProfileUpdate,
        UserPublic,
        UserSignup,
    )
    from ..utils.validation import ensure_password_length_limit, ensure_password_valid
except ImportError:
    from auth.dependencies import get_current_user, get_db
    from auth.security import create_access_token, hash_password, verify_password
    from auth.utils import to_user_public
    from models.database import User
    from models.schemas import (
        TokenResponse,
        UserLogin,
        UserProfileUpdate,
        UserPublic,
        UserSignup,
    )
    from utils.validation import ensure_password_length_limit, ensure_password_valid


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse)
def signup(payload: UserSignup, db: Session = Depends(get_db)) -> TokenResponse:
    """Create a user account and return an access token."""
    ensure_password_valid(payload.password)
    existing = db.query(User).filter(User.username == payload.username.strip()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(
        username=payload.username.strip(),
        name=payload.name.strip(),
        password_hash=hash_password(payload.password),
        age=payload.age,
        gender=payload.gender,
        state=payload.state,
        occupation=payload.occupation,
        income=payload.income,
        category=payload.category,
        disability=payload.disability,
        student_status=payload.student_status,
        farmer_status=payload.farmer_status,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(user.username)
    return TokenResponse(access_token=token, user=to_user_public(user))


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)) -> TokenResponse:
    """Authenticate a user and return an access token."""
    ensure_password_length_limit(payload.password)
    user = db.query(User).filter(User.username == payload.username.strip()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(user.username)
    return TokenResponse(access_token=token, user=to_user_public(user))


@router.get("/me", response_model=UserPublic)
def get_me(current_user: User = Depends(get_current_user)) -> UserPublic:
    """Return the current authenticated user."""
    return to_user_public(current_user)


@router.put("/profile", response_model=UserPublic)
def update_profile(
    payload: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserPublic:
    """Update the current authenticated user's profile."""
    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(current_user, key, value)

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return to_user_public(current_user)
