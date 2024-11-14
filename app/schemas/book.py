from pydantic import BaseModel

from .author import AuthorResponse


class Book(BaseModel):
    title: str
    author_id: int
    publication_year: int
    isbn: str


class BookResponse(BaseModel):
    id: int
    title: str
    author_id: int
    publication_year: int
    isbn: str
    author: AuthorResponse
