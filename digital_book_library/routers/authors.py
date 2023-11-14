from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List  
from ..database import SessionLocal
from ..models import Author, Book  
from ..utils import does_author_exist, verify_token

router = APIRouter()

# API to add an author
@router.post("/authors")
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