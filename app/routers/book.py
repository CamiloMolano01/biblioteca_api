from fastapi import APIRouter, Depends
from app.schemas.book import Book, BookResponse
from app.services.book_service import get_books, create_book, update_book, delete_book
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=list[BookResponse])
def get(
    title: str | None = None,
    author_name: str | None = None,
    author_id: int | None = None,
    publication_year: int | None = None,
    db: Session = Depends(get_db),
):
    return get_books(db, title, author_name, author_id, publication_year)


@router.post("/")
def add(book: Book, db: Session = Depends(get_db)):
    return create_book(db, book)


@router.put("/{id}")
def update(id: int, book: Book, db: Session = Depends(get_db)):
    return update_book(db, id, book)


@router.delete("/{id}", status_code=204)
def delete(id: int, db: Session = Depends(get_db)):
    return delete_book(db, id)
