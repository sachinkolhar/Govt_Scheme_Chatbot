"""Security helpers for password hashing and JWT handling."""
import base64
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

from jose import jwt

try:
    from ..config.settings import ACCESS_TOKEN_EXPIRE_HOURS, ALGORITHM, SECRET_KEY
except ImportError:
    from config.settings import ACCESS_TOKEN_EXPIRE_HOURS, ALGORITHM, SECRET_KEY


def hash_password(password: str) -> str:
    """Hash a password using PBKDF2-SHA256."""
    iterations = 390000
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return "pbkdf2_sha256${}${}${}".format(
        iterations,
        base64.urlsafe_b64encode(salt).decode("ascii"),
        base64.urlsafe_b64encode(digest).decode("ascii"),
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a stored hash."""
    if hashed_password.startswith("pbkdf2_sha256$"):
        try:
            _, iterations_s, salt_b64, digest_b64 = hashed_password.split("$", 3)
            iterations = int(iterations_s)
            salt = base64.urlsafe_b64decode(salt_b64.encode("ascii"))
            expected_digest = base64.urlsafe_b64decode(digest_b64.encode("ascii"))
            computed_digest = hashlib.pbkdf2_hmac(
                "sha256",
                plain_password.encode("utf-8"),
                salt,
                iterations,
            )
            return hmac.compare_digest(computed_digest, expected_digest)
        except Exception:
            return False

    if hashed_password.startswith("$2"):
        try:
            import bcrypt

            return bcrypt.checkpw(
                plain_password.encode("utf-8"),
                hashed_password.encode("utf-8"),
            )
        except Exception:
            return False

    return False


def create_access_token(username: str) -> str:
    """Create a JWT access token for a username."""
    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
