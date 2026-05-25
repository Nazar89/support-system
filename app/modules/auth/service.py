from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_token, verify_password
from app.modules.users.service import get_user_by_username


def login_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    return create_token(user.id)
