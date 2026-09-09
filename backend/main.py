from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from security import create_access_token, get_current_user, hash_password, verify_password
from database import Base, engine, get_session
import models

Base.metadata.create_all(engine)
app = FastAPI()


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)


class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    user_id: int


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=72)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Reading Tracker API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/books", response_model=list[BookResponse])
def list_books(title: str = "", db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    statement = select(models.Book).where(models.Book.user_id == current_user.id)
    if title != "":
        statement = statement.where(models.Book.title.contains(title))
    return db.scalars(statement).all()


@app.get("/books/{book_id}", response_model=BookResponse)
def show_book(book_id: int, db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    book = db.get(models.Book, book_id)
    if book is None or book.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books", response_model=BookResponse, status_code=201)
def create_book(book_in: BookCreate, db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    new_book = models.Book(title=book_in.title, user_id=current_user.id)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_in: BookCreate, db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    statement = select(models.Book).where(
        models.Book.id == book_id,
        models.Book.user_id == current_user.id
    )
    book = db.scalars(statement).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    book.title = book_in.title
    db.commit()
    db.refresh(book)
    return book

@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    statement = select(models.Book).where(
        models.Book.id == book_id,
        models.Book.user_id == current_user.id
    )
    book = db.scalars(statement).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return

@app.post("/signup", response_model=UserResponse, status_code=201)
def signup(user: UserCreate, session: Session = Depends(get_session)):
    statement = select(models.User).where(models.User.email == user.email)
    existing_user = session.scalars(statement).first()
    if existing_user is not None:
        raise HTTPException(status_code=409, detail="Email already registered")
    new_user = models.User(
        name=user.name, email=user.email, password=hash_password(user.password)
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@app.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, session: Session = Depends(get_session)):
    statement = select(models.User).where(models.User.email == credentials.email)
    user = session.scalars(statement).first()
    if user is None or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return TokenResponse(access_token=create_access_token(user.id))

@app.get("/books/{book_id}", response_model=BookResponse)
def read_book(book_id: int, session: Session = Depends(get_session),
              current_user: models.User = Depends(get_current_user)):
    book = session.get(models.Book, book_id)
    if book is None or book.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.get("/about")
async def read_about():
    return {
        "project": "This API allows users to track their reading progress.",
        "author": "Arthur Henrique",
    }
