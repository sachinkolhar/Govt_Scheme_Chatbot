import time

from fastapi.testclient import TestClient

import backend.main as main
from backend.auth.dependencies import SessionLocal
from backend.models.database import User


def _delete_user(username: str) -> None:
    with SessionLocal() as db:
        user = db.query(User).filter(User.username == username).first()
        if user:
            db.delete(user)
            db.commit()


def test_auth_signup_login_me_profile_flow() -> None:
    client = TestClient(main.app)
    username = f"auth_test_{int(time.time())}"
    password = "StrongPass1!"

    _delete_user(username)

    signup = client.post(
        "/auth/signup",
        json={
            "username": username,
            "name": "Auth Test User",
            "password": password,
            "age": 22,
            "state": "Karnataka",
        },
    )
    assert signup.status_code == 200
    signup_body = signup.json()
    assert signup_body["user"]["username"] == username

    login = client.post(
        "/auth/login",
        json={"username": username, "password": password},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    me = client.get("/auth/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["username"] == username

    profile = client.put(
        "/auth/profile",
        headers=headers,
        json={"occupation": "student", "student_status": True},
    )
    assert profile.status_code == 200
    assert profile.json()["occupation"] == "student"
    assert profile.json()["student_status"] is True

    _delete_user(username)
