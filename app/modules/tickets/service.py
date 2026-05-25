from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.tickets.models import Ticket
from app.modules.users.models import User

ALLOWED_STATUSES = {
    "open",
    "in_progress",
    "closed"
}


def create_ticket(db: Session, owner: User, title: str, description: str):
    ticket = Ticket(
        title=title,
        description=description,
        owner_id=owner.id,
        status="open"
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


def get_user_tickets(db: Session, owner: User):
    return db.query(Ticket).filter(Ticket.owner_id == owner.id).all()


def get_all_tickets(db: Session):
    return db.query(Ticket).all()


def get_ticket_by_id(db: Session, ticket_id: int):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    return ticket


def ensure_ticket_access(ticket: Ticket, user: User):
    if user.role in ("admin", "operator"):
        return

    if ticket.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )


def change_ticket_status(db: Session, ticket_id: int, new_status: str):
    if new_status not in ALLOWED_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ticket status"
        )

    ticket = get_ticket_by_id(db, ticket_id)
    ticket.status = new_status

    db.commit()
    db.refresh(ticket)

    return ticket
