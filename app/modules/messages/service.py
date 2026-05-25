from sqlalchemy.orm import Session

from app.modules.messages.models import Message
from app.modules.tickets.service import ensure_ticket_access, get_ticket_by_id
from app.modules.users.models import User


def create_message(
    db: Session,
    ticket_id: int,
    sender: User,
    text: str
):
    ticket = get_ticket_by_id(db, ticket_id)
    ensure_ticket_access(ticket, sender)

    message = Message(
        ticket_id=ticket_id,
        sender_id=sender.id,
        text=text
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_ticket_messages(db: Session, ticket_id: int, user: User):
    ticket = get_ticket_by_id(db, ticket_id)
    ensure_ticket_access(ticket, user)

    return db.query(Message).filter(Message.ticket_id == ticket_id).all()
