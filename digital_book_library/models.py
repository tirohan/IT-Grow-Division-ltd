from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://username:password@localhost/digital_library"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, unique=True)
    birth_date = Column(Date)
    biography = Column(String)

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author")
    publication_date = Column(Date)
    genre = Column(String)
    isbn = Column(String, unique=True)

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, unique=True)
    email = Column(String)
    address = Column(String)