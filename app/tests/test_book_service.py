from fastapi import HTTPException
from app.models.models import Author
from app.schemas.book import Book
from app.services.book_service import (
    create_book,
    get_book,
    delete_book,
    update_book,
    get_books,
)


def create_author(db_session):
    author1 = Author(name="Gabriel García Márquez")
    db_session.add(author1)
    db_session.commit()
    return author1


# -------------------------------------------------------------------------
# ---
# Test the create_book function
# ---


def test_create_book(db_session):
    author1 = create_author(db_session)
    payload = {
        "title": "Test Book",
        "author_id": author1.id,
        "publication_year": 2024,
        "isbn": "978-3-16-148410-57",
    }
    book_data = Book(**payload)

    response = create_book(db_session, book_data)
    assert response.title == "Test Book"
    assert response.author_id == author1.id
    assert response.publication_year == 2024
    assert response.isbn == "978-3-16-148410-57"


def test_create_book_duplicate_isbn(db_session):
    author = create_author(db_session)
    payload = {
        "title": "Test Book",
        "author_id": author.id,
        "publication_year": 2024,
        "isbn": "978-3-16-148410-14",
    }
    book_data1 = Book(**payload)

    create_book(db_session, book_data1)
    try:
        create_book(db_session, book_data1)
    except HTTPException as e:
        assert e.status_code == 409
        assert e.detail == "A book with this ISBN already exists."


def test_create_book_invalid_author(db_session):
    payload = {
        "title": "Test Book",
        "author_id": 171899,
        "publication_year": 2024,
        "isbn": "978-3-16-148410-14",
    }

    try:
        create_book(db_session, Book(**payload))
    except HTTPException as e:
        assert e.status_code == 400
        assert e.detail == "The specified author ID does not exist."


# -------------------------------------------------------------------------
# ---
# Test the get_books function
# ---


def prepare_get_books(db_session):
    author1 = create_author(db_session)
    author2 = Author(name="Jorge Luis Borges")
    db_session.add(author2)
    db_session.commit()

    payload1 = {
        "title": "Cien años de soledad",
        "author_id": author1.id,
        "publication_year": 1967,
        "isbn": "978-3-16-148411-5",
    }
    payload2 = {
        "title": "Ficciones",
        "author_id": author2.id,
        "publication_year": 1944,
        "isbn": "978-3-16-148411-7",
    }
    payload3 = {
        "title": "El Aleph",
        "author_id": author2.id,
        "publication_year": 1923,
        "isbn": "978-3-16-148413-7",
    }
    payload4 = {
        "title": "1969",
        "author_id": author2.id,
        "publication_year": 1923,
        "isbn": "978-3-16-148414-7",
    }
    payload5 = {
        "title": "El amor en los tiempos del cólera",
        "author_id": author1.id,
        "publication_year": 1985,
        "isbn": "978-3-16-148415-5",
    }

    create_book(db_session, Book(**payload1))
    create_book(db_session, Book(**payload2))
    create_book(db_session, Book(**payload3))
    create_book(db_session, Book(**payload4))
    create_book(db_session, Book(**payload5))

    return author1, author2


def test_get_all_books(db_session):
    prepare_get_books(db_session)
    books = get_books(db_session)
    assert len(books) == 5


def test_get_books_by_title(db_session):
    prepare_get_books(db_session)
    books = get_books(db_session, title="Cien años de soledad")
    assert len(books) == 1
    assert books[0].title == "Cien años de soledad"


def test_get_books_by_title_insensitive(db_session):
    prepare_get_books(db_session)
    books = get_books(db_session, title="cien años de soledad")
    assert len(books) == 1
    assert books[0].title == "Cien años de soledad"


def test_get_books_by_title_partial(db_session):
    prepare_get_books(db_session)
    books = get_books(db_session, title="soledad")
    assert len(books) == 1
    assert books[0].title == "Cien años de soledad"


def test_get_books_by_author_name(db_session):
    prepare_get_books(db_session)
    booksJorge = get_books(db_session, author_name="Jorge Luis Borges")
    assert len(booksJorge) == 3
    booksGabriel = get_books(db_session, author_name="Gabriel García Márquez")
    assert len(booksGabriel) == 2


def test_get_books_by_author_name_insensitive(db_session):
    prepare_get_books(db_session)
    booksJorge = get_books(db_session, author_name="jorge luis borges")
    assert len(booksJorge) == 3
    booksGabriel = get_books(db_session, author_name="gabriel garcía márquez")
    assert len(booksGabriel) == 2


def test_get_books_by_author_name_partial(db_session):
    prepare_get_books(db_session)
    booksJorge = get_books(db_session, author_name="Borges")
    assert len(booksJorge) == 3
    booksGabriel = get_books(db_session, author_name="Márquez")
    assert len(booksGabriel) == 2


def test_get_books_by_author_id(db_session):
    author1, author2 = prepare_get_books(db_session)
    author = create_author(db_session)
    booksNewAuthor = get_books(db_session, author_id=author.id)
    assert len(booksNewAuthor) == 0
    booksGabriel = get_books(db_session, author_id=author1.id)
    assert len(booksGabriel) == 2
    booksJorge = get_books(db_session, author_id=author2.id)
    assert len(booksJorge) == 3


def test_get_books_by_publication_year(db_session):
    prepare_get_books(db_session)
    books1967 = get_books(db_session, publication_year=1967)
    assert len(books1967) == 1
    assert books1967[0].publication_year == 1967
    books1923 = get_books(db_session, publication_year=1923)
    assert len(books1923) == 2
    assert books1923[0].publication_year == 1923
    assert books1923[1].publication_year == 1923


# -------------------------------------------------------------------------
# ---
# Test the get_book function
# ---


def test_get_book_not_found(db_session):
    try:
        get_book(db_session, 99999)
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Book not found"


# -------------------------------------------------------------------------
# ---
# Test the delete_book function
# ---


def test_delete_book(db_session):
    author = create_author(db_session)
    payload = {
        "title": "Test Book",
        "author_id": author.id,
        "publication_year": 2024,
        "isbn": "978-3-16-148410-7",
    }

    createdBookId = create_book(db_session, Book(**payload)).id
    try:
        delete_book(db_session, createdBookId)
    except HTTPException as e:
        assert e.status_code == 204
        assert e.detail == "No Content"


# -------------------------------------------------------------------------
# ---
# Test the update_book function
# ---


def test_update_book(db_session):
    author = create_author(db_session)
    payload = {
        "author_id": author.id,
        "publication_year": 2024,
        "isbn": "978-3-16-148410-7",
    }

    created_book = create_book(db_session, Book(**payload, title="Test Book"))
    assert created_book.title == "Test Book"
    updated_book = update_book(
        db_session, created_book.id, Book(**payload, title="Updated Book")
    )
    assert updated_book.title == "Updated Book"
    assert updated_book.id == created_book.id
