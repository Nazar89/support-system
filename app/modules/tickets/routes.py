from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user, require_role
from app.database import get_db
from app.modules.tickets.schemas import TicketCreate, TicketRead, TicketStatusUpdate
from app.modules.tickets.service import (
    change_ticket_status,
    create_ticket,
    ensure_ticket_access,
    get_all_tickets,
    get_ticket_by_id,
    get_user_tickets,
)
from app.modules.users.models import User

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post("/", response_model=TicketRead)
def create_new_ticket(
    data: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_ticket(db, current_user, data.title, data.description)


@router.get("/my", response_model=list[TicketRead])
def list_my_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_tickets(db, current_user)


@router.get("/", response_model=list[TicketRead])
def list_all_tickets(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin", "operator"))
):
    return get_all_tickets(db)


@router.get("/{ticket_id}", response_model=TicketRead)
def read_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ticket = get_ticket_by_id(db, ticket_id)
    ensure_ticket_access(ticket, current_user)
    return ticket


@router.patch("/{ticket_id}/status", response_model=TicketRead)
def update_ticket_status(
    ticket_id: int,
    data: TicketStatusUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin", "operator"))
):
    return change_ticket_status(db, ticket_id, data.status)
