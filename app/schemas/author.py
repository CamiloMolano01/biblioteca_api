from pydantic import BaseModel


class Author(BaseModel):
    name: str


class AuthorResponse(BaseModel):
    id: int
    name: str
