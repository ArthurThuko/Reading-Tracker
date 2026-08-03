from sqlmodel import Field, SQLModel, Relationship

class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    pages: int
    author_id: int = Field(foreign_key="author.id")
    user_id: int = Field(foreign_key="user.id")
    
    user: User | None = Relationship(back_populates="books")
    author: Author | None = Relationship(back_populates="books")