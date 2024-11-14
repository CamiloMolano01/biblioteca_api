from sqlalchemy.orm import Session
from .models.models import Author, Book


def load_sample_data(session: Session):
    authors_exist = session.query(Author).first()
    if authors_exist:
        return

    author1 = Author(name="Gabriel García Márquez")
    author2 = Author(name="Isabel Allende")
    author3 = Author(name="Mario Vargas Llosa")

    book1 = Book(
        title="Cien Años de Soledad",
        isbn="BAC100",
        publication_year=1967,
        author=author1,
    )
    book2 = Book(
        title="El Amor en los Tiempos del Cólera",
        isbn="ELA200",
        publication_year=1985,
        author=author1,
    )
    book3 = Book(
        title="La Casa de los Espíritus",
        isbn="LCE300",
        publication_year=1982,
        author=author2,
    )
    book4 = Book(
        title="La Ciudad y los Perros",
        isbn="LCY4s00",
        publication_year=1963,
        author=author3,
    )

    session.add_all([author1, author2, book1, book2, book3, book4])
    session.commit()
