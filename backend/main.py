from fastapi import FastAPI

app = FastAPI()

books = [
    {"id": 0, "title": "Clean Code"},
    {"id": 1, "title": "Refactoring"},
]

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Reading Tracker API"}

@app.get("/health")
def home(page:int = 1, title:str = ""):
    print(page, title)
    return {"Message": "Ok"}

@app.get("/books")
def list_books():
    return books

@app.post("/books")
def create_book(book: dict):
    new_book = {"id": len(books) + 1, "name": book["name"]}
    books.append(new_book)
    return new_book

@app.get("/books/{id}")
def show_book(id: int):
    return books[id]

@app.get("/about")
async def read_about():
    return {
        "project": "This API allows users to track their reading progress and manage their reading lists.",
        "author": "Arthur Henrique",
    }