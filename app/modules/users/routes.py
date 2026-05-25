from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user, require_role
from app.database import get_db
from app.modules.users.models import User
from app.modules.users.schemas import UserCreate, UserRead, UserRoleUpdate
from app.modules.users.service import create_user, get_all_users, change_user_role

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserRead)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    return create_user(
        db=db,
        username=data.username,
        email=data.email,
        password=data.password,
        role=data.role
    )


@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=list[UserRead])
def list_users(
    db: Session = Depends(get_db),
    admin: User = Depends(require_role("admin"))
):
    return get_all_users(db)


@router.patch("/{user_id}/role", response_model=UserRead)
def update_role(
    user_id: int,
    data: UserRoleUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role("admin"))
):
    return change_user_role(db, user_id, data.role)
