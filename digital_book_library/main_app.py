from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session

app = FastAPI()

DATABASE_URL = "postgresql://username:password@localhost/digital_library"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

security = OAuth2PasswordBearer(tokenUrl="token")
ALGORITHM = "HS256"

import secrets
SECRET_KEY = secrets.token_urlsafe(32)

# Data Models
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

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Token expires in 15 minutes
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def does_author_exist(author_id: int, db: Session):
    author = db.query(Author).filter(Author.id == author_id).first()
    return author is not None

def verify_token(token: str = Depends(security)):
    try:
        # Verify the token using your secret key
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Extract the expiration time from the token's payload
        exp = payload.get("exp")
        
        # Check if the token has expired
        current_time = datetime.utcnow()
        if current_time > datetime.fromtimestamp(exp):
            raise HTTPException(status_code=401, detail="Token has expired")

        # You can perform additional checks on the payload if needed
        return True
    except JWTError:
        # Token is invalid, raise an HTTPException
        raise HTTPException(status_code=401, detail="Invalid token")

# API to add a book
@app.post("/books")
async def add_book(book: Book, token: str = Depends(verify_token)):
    # Verify the token for authorization
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        # Ensure the author exists in the database (you can implement this check)
        author_exists = does_author_exist(book.author_id)
        if not author_exists:
            raise HTTPException(status_code=400, detail="Author not found")

        # Create the new book and link it to the author
        new_book = Book(title=book.title, author_id=book.author_id)
        db = SessionLocal()
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        db.close()
        return new_book
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# API to add an author
@app.post("/authors")
async def add_author(author: Author, token: str = Depends(verify_token)):
    # Verify the token for authorization
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        new_author = Author(full_name=author.full_name)
        db = SessionLocal()
        db.add(new_author)
        db.commit()
        db.refresh(new_author)
        db.close()
        return new_author
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@app.put("/books/{book_id}")
async def edit_book(book_id: int, new_title: str, new_author_id: int, token: str = Depends(verify_token)):
    # Edit the book's title and author
    # Verify the token for authorization (placeholder)
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        db = SessionLocal()
        book = db.query(Book).filter(Book.id == book_id).first()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        if new_title:
            book.title = new_title
        if new_author_id:
            author_exists = does_author_exist(new_author_id)
            if not author_exists:
                raise HTTPException(status_code=400, detail="Author not found")
            book.author_id = new_author_id

        db.commit()
        db.refresh(book)
        db.close()
        return book
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# API to retrieve books with filtering options
@app.get("/books")
async def retrieve_books(starts_with: str = None, author_id: int = None):
    try:
        db = SessionLocal()
        query = db.query(Book)
        if starts_with:
            query = query.filter(Book.title.startswith(starts_with))
        if author_id:
            query = query.filter(Book.author_id == author_id)
        
        books = query.all()
        db.close()
        return books
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# API to add multiple books by the same author
@app.post("/authors/{author_id}/add-books")
async def add_multiple_books_by_author(author_id: int, book_titles: List[str], token: str = Depends(verify_token)):
    # Add multiple books by the same author
    # Verify the token for authorization (placeholder)
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        author_exists = does_author_exist(author_id)
        if not author_exists:
            raise HTTPException(status_code=400, detail="Author not found")

        db = SessionLocal()
        for title in book_titles:
            new_book = Book(title=title, author_id=author_id)
            db.add(new_book)
        db.commit()
        db.close()
        return {"message": "Books added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# API to create a client
@app.post("/clients")
async def create_client(client_name: str, token: str = Depends(verify_token)):
    # Create a client
    # Verify the token for authorization (placeholder)
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        new_client = Client(full_name=client_name)
        db = SessionLocal()
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        db.close()
        return new_client
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# API to retrieve books borrowed by a client
@app.get("/clients/{client_id}/borrowed-books")
async def retrieve_books_borrowed_by_client(client_id: int, token: str = Depends(verify_token)):
    # Retrieve a list of books borrowed by the client
    # Verify the token for authorization (placeholder)
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        db = SessionLocal()
        books = db.query(Book).join(Client).filter(Client.id == client_id).all()
        db.close()
        return books
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# API to link a client to a book (client borrowed the book)
@app.post("/clients/{client_id}/borrow-book/{book_id}")
async def link_client_to_book(client_id: int, book_id: int, token: str = Depends(verify_token)):
    # Link a client to a book (client borrowed the book)
    # Verify the token for authorization (placeholder)
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        db = SessionLocal()
        client = db.query(Client).filter(Client.id == client_id).first()
        book = db.query(Book).filter(Book.id == book_id).first()
        if client is None or book is None:
            raise HTTPException(status_code=404, detail="Client or book not found")

        client.borrowed_books.append(book)
        db.commit()
        db.close()
        return {"message": "Book linked to the client successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# API to unlink a client from a book (client returned the book)
@app.delete("/clients/{client_id}/return-book/{book_id}")
async def unlink_client_from_book(client_id: int, book_id: int, token: str = Depends(verify_token)):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        db = SessionLocal()
        client = db.query(Client).filter(Client.id == client_id).first()
        book = db.query(Book).filter(Book.id == book_id).first()
        if client is None or book is None:
            raise HTTPException(status_code=404, detail="Client or book not found")

        if book in client.borrowed_books:
            client.borrowed_books.remove(book)
            db.commit()
            db.close()
            return {"message": "Book unlinked from the client successfully"}
        else:
            raise HTTPException(status_code=404, detail="Book not found in client's borrowed books")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

