from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.faq.models import FAQ


def create_faq(db: Session, question: str, answer: str):
    item = FAQ(
        question=question,
        answer=answer
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def get_all_faq(db: Session):
    return db.query(FAQ).all()


def delete_faq(db: Session, faq_id: int):
    item = db.query(FAQ).filter(FAQ.id == faq_id).first()

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="FAQ item not found"
        )

    db.delete(item)
    db.commit()
