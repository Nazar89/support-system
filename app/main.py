from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine, SessionLocal

from app.modules.users.models import User
from app.modules.tickets.models import Ticket
from app.modules.messages.models import Message
from app.modules.faq.models import FAQ

from app.modules.users.service import create_user, get_user_by_username

from app.modules.auth.routes import router as auth_router
from app.modules.users.routes import router as users_router
from app.modules.tickets.routes import router as tickets_router
from app.modules.messages.routes import router as messages_router
from app.modules.faq.routes import router as faq_router
from app.modules.admin.routes import router as admin_router

app = FastAPI(title="Technical Support System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


def create_default_admin():
    db = SessionLocal()
    try:
        admin = get_user_by_username(db, "admin")
        if admin is None:
            create_user(
                db=db,
                username="admin",
                email="admin@example.com",
                password="admin123",
                role="admin"
            )
    finally:
        db.close()


create_default_admin()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(tickets_router)
app.include_router(messages_router)
app.include_router(faq_router)
app.include_router(admin_router)

app.mount("/", StaticFiles(directory="static", html=True), name="static")