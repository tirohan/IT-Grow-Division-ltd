from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Book
from ..utils import does_author_exist, verify_token
from typing import List


router = APIRouter()

# API to edit a book
@router.put("/books/{book_id}")
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
@router.get("/books")
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
@router.post("/authors/{author_id}/add-books")
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