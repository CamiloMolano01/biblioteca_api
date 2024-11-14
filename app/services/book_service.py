import unicodedata
from fastapi import HTTPException
from app.models.models import Author, Book
from app.schemas.book import Book as BookSchema
from sqlalchemy.orm import Session
from sqlalchemy import func


def remove_accents(input_str: str) -> str:
    nfkd_form = unicodedata.normalize("NFKD", input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


def get_book(db: Session, id: int):
    book = db.query(Book).filter(Book.id == id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


def get_books(
    db: Session,
    title: str | None = None,
    author_name: str | None = None,
    author_id: int | None = None,
    publication_year: int | None = None,
):
    query = db.query(Book).join(Author, Book.author_id == Author.id)

    if title:
        normalized_title = remove_accents(title)
        query = query.filter(func.unaccent(Book.title).ilike(f"%{normalized_title}%"))
    if author_id:
        query = query.filter(Book.author_id == author_id)
    if publication_year:
        query = query.filter(Book.publication_year == publication_year)
    if author_name:
        normalized_author = remove_accents(author_name)
        query = query.filter(func.unaccent(Author.name).ilike(f"%{normalized_author}%"))
    return query.all()


def create_book(db: Session, book: BookSchema):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, id: int, book: BookSchema):
    db_book = get_book(db, id)
    for key, value in book.model_dump().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, id: int):
    db_book = get_book(db, id)
    db.delete(db_book)
    db.commit()
    raise HTTPException(status_code=204)
