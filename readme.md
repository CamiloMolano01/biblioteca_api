# Library API

This is a FastAPI-based library management API, designed for managing books and authors. It utilizes SQLAlchemy as an ORM to interact with a PostgreSQL database and provides Swagger for easy API documentation and testing.

## Technologies Used

- **FastAPI**: Web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **SQLAlchemy**: ORM for database interaction.
- **PostgreSQL**: Database used to store book and author data.
- **Pytest**: Testing framework for writing unit and integration tests.
- **Swagger**: Auto-generated API documentation.
- **Docker**: Containerization platform used to run the application and database.

## Features

- **CRUD operations** for managing books.
- **Swagger** documentation for easy exploration of the API.
- **Database integration** using SQLAlchemy ORM.
- **Automated tests** for API and database operations with Pytest.
- **Dockerized** application and PostgreSQL database for easy deployment.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/CamiloMolano01/biblioteca_api.git
   cd biblioteca-api
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database by running migrations or create the tables:

   ```bash
   alembic upgrade head
   ```

   Tables will be created automatically when the app starts.

5. Run the application:

   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`.

## Docker Compose

To use Docker for both the application and the database, you need a Docker Compose setup. This is useful for simplifying the local development environment.

- The `docker-compose.yml` file will configure both the application and the PostgreSQL database.

- To start the Docker containers, run:

  ```bash
  docker-compose up --build
  ```

- The API will be available at `http://localhost:8000`, and the database will be set up inside the Docker container.

## API Documentation

Once the app is running, you can access the Swagger UI at:

- [Swagger Documentation](http://localhost:8000/docs)

The Swagger interface will provide easy access to all the endpoints and allow you to interact with the API directly.

## Testing

The project uses **Pytest** for testing. To run tests, first run the docker compose inside the repostory (for the databases) and use the following command:

```bash
pytest
```

The tests are designed to verify both the API endpoints and the database operations, ensuring that the application behaves as expected.

To view the coverage use the following command:

```bash
pytest --cov=app app/tests/
```

### Example Tests

- **Test book creation**: Tests the creation of a new book.
- **Test error handling**: Tests for various error cases such as duplicate ISBN or missing author.

## Database Setup

The application uses a PostgreSQL database. The database connection URL is defined in the `app/database.py` file. For local development, the default configuration uses the `library` database.

You can modify the `SQLALCHEMY_DATABASE_URL` in the configuration file to connect to different databases or use Docker to spin up a PostgreSQL container.

## Code Structure

- `app/main.py`: The main FastAPI app and route definitions.
- `app/database.py`: Database configuration and SQLAlchemy models.
- `app/models/models.py`: SQLAlchemy models for the Book and Author entities.
- `app/schemas`: Pydantic models (schemas) used for request and response validation.
- `app/routers`: Functions that handle the endpoints.
- `app/services/book_service.py`: Functions that handle CRUD operations.
- `app/tests`: Contains the test files and fixtures.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.