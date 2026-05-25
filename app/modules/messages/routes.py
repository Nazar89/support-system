from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database import get_db
from app.modules.messages.schemas import MessageCreate, MessageRead
from app.modules.messages.service import create_message, get_ticket_messages
from app.modules.users.models import User

router = APIRouter(prefix="/tickets/{ticket_id}/messages", tags=["Messages"])


@router.post("/", response_model=MessageRead)
def send_message(
    ticket_id: int,
    data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_message(db, ticket_id, current_user, data.text)


@router.get("/", response_model=list[MessageRead])
def list_messages(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_ticket_messages(db, ticket_id, current_user)
