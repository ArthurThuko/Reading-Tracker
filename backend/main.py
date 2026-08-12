from fastapi import FastAPI, HTTPException
from backend.book import Book

app = FastAPI()

books = [
    Book(id=0, name="Clean Code"),
    Book(id=1, name="Refactoring"),
    Book(id=2, name="The Pragmatic Programmer"),
]

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Reading Tracker API"}

@app.get("/health")
def test_url(page:int = 1, title:str = ""):
    print(page, title)
    return {"Message": "Ok"}

@app.get("/books")
def list_books():
    return books

@app.post("/books")
def create_book(book: dict):
    if not book.get("name"):
        raise HTTPException(status_code=500, detail="Formato não aceito")
    new_book = Book(id=len(books), name=book["name"])
    books.append(new_book)
    return new_book

@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    for book in books:
        if book.id == book_id:
            books.remove(book)
            return
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/{book_id}")
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