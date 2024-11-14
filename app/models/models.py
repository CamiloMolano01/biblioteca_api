from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer(), primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    books = relationship("Book", backref="author")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer(), primary_key=True, index=True)
    isbn = Column(String(100), nullable=False, unique=True, index=True)
    title = Column(String(100), nullable=False, index=True)
    publication_year = Column(Integer(), nullable=False, index=True)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    author_id = Column(Integer(), ForeignKey("authors.id"))
