import sqlalchemy
from sqlalchemy import (Column, Date, Integer, Sequence, String, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Author(Base):
    __tablename__ = 'authors'
    id = Column(String, primary_key=True)
    pen_name = Column(String)


class Book(Base):
    __tablename__ = 'books'
    id = Column(String, primary_key=True)  # isbn
    title = Column(String)
    date = Column(Date, nullable=True)


def init_db():
    db_engine = create_engine('sqlite:///:memory:')

    Base.metadata.create_all(db_engine)

    DBSession = sessionmaker() 
    DBSession.configure(bind=db_engine)

    return db_engine, DBSession
