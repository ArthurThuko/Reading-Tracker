from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import Base, engine, get_session
import models

Base.metadata.create_all(engine)
app = FastAPI()

class BookCreate(BaseModel):
    title: str

class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Reading Tracker API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/books", response_model=list[BookResponse])
def list_books(title: str = "", db: Session = Depends(get_session)):
    statement = select(models.Book)
    if title != "":
        statement = statement.filter(models.Book.title.contains(title))
    return db.execute(statement).scalars().all()

@app.get("/books/{book_id}", response_model=BookResponse)
def show_book(book_id: int, db: Session = Depends(get_session)):
    book = db.get(models.Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books", response_model=BookResponse, status_code=201)
def create_book(book_in: BookCreate, db: Session = Depends(get_session)):
    new_book = models.Book(title=book_in.title)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_in: BookCreate, db: Session = Depends(get_session)):
    book = db.get(models.Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    book.title = book_in.title
    db.commit()
    db.refresh(book)
    return book


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_session)):
    book = db.get(models.Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return


@app.get("/about")
async def read_about():
    return {
        "project": "This API allows users to track their reading progress.",
        "author": "Arthur Henrique",
    }