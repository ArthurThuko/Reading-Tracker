from fastapi import Depends, FastAPI, HTTPException
from database import Base, engine, get_session
import models

Base.metadata.create_all(engine)
app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Reading Tracker API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/books", response_model=list[Book])
def list_books():
    return books

@app.post("/books", response_model=Book, status_code=201)
def create_book(book_in: BookCreate):
    global next_book_id
    new_book = Book(id=next_book_id, name=book_in.name)
    next_book_id += 1
    books.append(new_book)
    return new_book

@app.get("/books/{book_id}", response_model=models.Book)
def show_book(book_id: int):
    for book in book:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.put("/books/{book_id}", response_model=models.Book)
def update_book(book_id: int, book_in: BookCreate):
    for book in book:
        if book.id == book_id:
            book.name = book_in.name
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    for book in book:
        if book.id == book_id:
            book.remove(book)
            return
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/about")
async def read_about():
    return {
        "project": "This API allows users to track their reading progress.",
        "author": "Arthur Henrique",
    }