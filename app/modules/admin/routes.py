from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import require_role
from app.database import get_db
from app.modules.messages.models import Message
from app.modules.tickets.models import Ticket
from app.modules.users.models import User

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/stats")
def get_system_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(require_role("admin"))
):
    users_count = db.query(User).count()
    tickets_count = db.query(Ticket).count()
    messages_count = db.query(Message).count()

    tickets_by_status = {}

    for ticket in db.query(Ticket).all():
        tickets_by_status[ticket.status] = tickets_by_status.get(ticket.status, 0) + 1

    return {
        "users_count": users_count,
        "tickets_count": tickets_count,
        "messages_count": messages_count,
        "tickets_by_status": tickets_by_status
    }
