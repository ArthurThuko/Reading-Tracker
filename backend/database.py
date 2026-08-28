from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

DATABASE_URL = "mysql+pymysql://root:ar120604@127.0.0.1/reading_tracker"

engine = create_engine(DATABASE_URL, echo=True)

class Base(DeclarativeBase):
    pass

def get_session():
    with Session(engine) as session:
        yield session