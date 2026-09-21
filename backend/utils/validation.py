"""
Validation utilities for password and input validation.
"""
import re
from fastapi import HTTPException


def ensure_password_length_limit(password: str) -> None:
    """
    Validate password doesn't exceed bcrypt's 72-byte limit.
    
    Args:
        password: Password string to validate
        
    Raises:
        HTTPException: If password exceeds 72 bytes
    """
    if len(password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password is too long. Please keep your password to 72 characters or fewer.",
        )


def ensure_password_policy(password: str) -> None:
    """
    Validate password meets policy requirements:
    - At least 8 characters
    - At least 1 uppercase letter
    - At least 1 number
    - At least 1 special character
    
    Args:
        password: Password string to validate
        
    Raises:
        HTTPException: If password doesn't meet policy
    """
    if len(password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters long.",
        )

    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must include at least 1 uppercase letter.",
        )

    if not re.search(r"\d", password):
        raise HTTPException(
            status_code=400,
            detail="Password must include at least 1 number.",
        )

    if not re.search(r"[^A-Za-z0-9]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must include at least 1 special character.",
        )


def ensure_password_valid(password: str) -> None:
    """
    Run all password validation checks.
    
    Args:
        password: Password string to validate
        
    Raises:
        HTTPException: If password fails any validation check
    """
    ensure_password_length_limit(password)
    ensure_password_policy(password)
