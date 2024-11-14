from fastapi import FastAPI
from app.routers import book
from .database import init_db

app = FastAPI()

init_db()

app.include_router(book.router, prefix="/books", tags=["books"])
