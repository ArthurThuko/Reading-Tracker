from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from book import Book

app = FastAPI()

books = [
    Book(id=0, name="Clean Code"),
    Book(id=1, name="Refactoring"),
    Book(id=2, name="The Pragmatic Programmer"),
]

next_book_id = len(books)

class Book(BaseModel):
    id: int
    name: str

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Reading Tracker API"}

@app.get("/health")
def test_url(page:int = 1, title:str = ""):
    print(page, title)
    return {"Message": "Ok"}

@app.get("/books", response_model=list[Book])
def list_books():
    return books

@app.post("/books", response_model=Book, status_code=201)
def create_book(book: Book):
    global next_book_id
    new_book = Book(id=next_book_id, name=book.name)
    next_book_id += 1
    books.append(new_book)
    return new_book

@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    for book in books:
        if book.id == book_id:
            books.remove(book)
            return
    raise HTTPException(status_code=404, detail="Book not found")

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: Book):
    for stored_book in books:
        if stored_book.id == book_id:
            stored_book.name = book.name
            return stored_book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/{book_id}", response_model=Book)
def show_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/about")
async def read_about():
    return {
        "project": "This API allows users to track their reading progress and manage their reading lists.",
        "author": "Arthur Henrique",
    }