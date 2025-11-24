from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Input model when adding a new book
class BookIn(BaseModel):
    title: str
    author: str
    year: Optional[int] = None


# Model stored in memory (includes ID)
class Book(BookIn):
    id: int


# Initial books list (added by default)
books: List[Book] = [
    Book(id=1, title="Clean Code", author="Robert C. Martin", year=2008),
    Book(id=2, title="The Pragmatic Programmer", author="Andrew Hunt", year=1999),
    Book(id=3, title="Introduction to Algorithms", author="Thomas H. Cormen", year=2009)
]

# Counter to assign new IDs
counter = 4




@app.get("/books", response_model=List[Book])
def get_books():
    """
    Return the full list of books.
    """
    return books


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    """
    Return a single book by ID.
    Raise 404 error if not found.
    """
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/books", response_model=Book, status_code=201)
def add_book(book: BookIn):
    """
    Add a new book.
    Automatically assigns the next available ID.
    """
    global counter
    new_book = Book(id=counter, **book.dict())
    books.append(new_book)
    counter += 1
    return new_book


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    """
    Delete a book by its ID.
    Raises 404 if the book does not exist.
    """
    for book in books:
        if book.id == book_id:
            books.remove(book)
            return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")

