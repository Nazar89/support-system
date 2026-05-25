from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import require_role
from app.database import get_db
from app.modules.faq.schemas import FAQCreate, FAQRead
from app.modules.faq.service import create_faq, delete_faq, get_all_faq
from app.modules.users.models import User

router = APIRouter(prefix="/faq", tags=["FAQ"])


@router.get("/", response_model=list[FAQRead])
def list_faq(db: Session = Depends(get_db)):
    return get_all_faq(db)


@router.post("/", response_model=FAQRead)
def add_faq(
    data: FAQCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role("admin"))
):
    return create_faq(db, data.question, data.answer)


@router.delete("/{faq_id}")
def remove_faq(
    faq_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role("admin"))
):
    delete_faq(db, faq_id)
    return {"message": "FAQ item deleted"}
