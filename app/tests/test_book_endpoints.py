from app.models.models import Author


def create_author(db_session):
    author1 = Author(name="Gabriel García Márquez")
    db_session.add(author1)
    db_session.commit()
    return author1


def test_create_book(client, db_session):
    author1 = create_author(db_session)

    payload = {
        "title": "Test Book",
        "author_id": author1.id,
        "publication_year": 2024,
        "isbn": "978-3-16-148410-5",
    }

    response = client.post("/books/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["author_id"] == author1.id
    assert data["publication_year"] == 2024
    assert data["isbn"] == "978-3-16-148410-5"


def test_create_book_duplicate_isbn(client, db_session):
    author = create_author(db_session)
    payload = {
        "title": "Test Book",
        "author_id": author.id,
        "publication_year": 2024,
        "isbn": "978-3-16-148410-14",
    }

    response = client.post("/books/", json=payload)
    assert response.status_code == 201
    response2 = client.post("/books/", json=payload)
    assert response2.json()["detail"] == "A book with this ISBN already exists."
    assert response2.status_code == 409


def test_create_book_unproccessable(client):
    payload = {"title": "Test Book", "author_id": 1, "publication_year": 2024}

    response = client.post("/books/", json=payload)
    assert response.status_code == 422


def test_get_book_not_found(client):
    response = client.get("/books/99999")
    assert response.status_code == 404


def test_update_book(client, db_session):
    author = create_author(db_session)
    payload = {
        "title": "Test Book",
        "author_id": author.id,
        "publication_year": 2024,
        "isbn": "978-3-16-148410-14",
    }

    payload_updated = {
        "title": "Test Book Updated",
        "author_id": author.id,
        "publication_year": 2025,
        "isbn": "978-3-16-148410-14",
    }

    response = client.post("/books/", json=payload)
    assert response.status_code == 201
    responseId = response.json()["id"]
    assert response.json()["title"] == "Test Book"
    assert response.json()["publication_year"] == 2024
    response = client.put(f"/books/{responseId}", json=payload_updated)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book Updated"
    assert response.json()["publication_year"] == 2025


def test_update_book_not_found(client):
    payload = {
        "title": "Test Book",
        "author_id": 1,
        "publication_year": 2024,
        "isbn": "978-3-16-148410-0",
    }

    response = client.put("/books/99999", json=payload)
    assert response.status_code == 404


def test_update_book_unproccessable(client):
    payload = {"title": "Test Book", "author_id": "id", "publication_year": 2024}

    response = client.put("/books/1", json=payload)
    assert response.status_code == 422


def test_delete_book(client, db_session):
    author = create_author(db_session)
    payload = {
        "title": "Test Book",
        "author_id": author.id,
        "publication_year": 2024,
        "isbn": "978-3-16-148410-7",
    }

    createdBookId = client.post("/books/", json=payload).json()["id"]
    response = client.delete(f"/books/{createdBookId}")
    assert response.status_code == 204
    book = client.get(f"/books/{createdBookId}")
    assert book.status_code == 404


def test_delete_book_not_found(client):
    response = client.delete("/books/99999")
    assert response.status_code == 404
