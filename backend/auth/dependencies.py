"""Authentication dependencies and shared FastAPI helpers."""
from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

try:
    from ..config.database import SessionLocal
    from ..config.settings import ALGORITHM, SECRET_KEY
    from ..models.database import User
except ImportError:
    from config.database import SessionLocal
    from config.settings import ALGORITHM, SECRET_KEY
    from models.database import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db() -> Generator[Session, None, None]:
    """Provide a database session for request scope."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Resolve the currently authenticated user from a bearer token."""
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise unauthorized
    except JWTError as exc:
        raise unauthorized from exc

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise unauthorized
    return user
