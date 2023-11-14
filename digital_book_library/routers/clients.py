from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Client, Book  
from ..utils import verify_token  

router = APIRouter()

# API to create a client
@router.post("/clients")
async def create_client(client_name: str, token: str = Depends(verify_token)):
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
@router.get("/clients/{client_id}/borrowed-books")
async def retrieve_books_borrowed_by_client(client_id: int, token: str = Depends(verify_token)):
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
@router.post("/clients/{client_id}/borrow-book/{book_id}")
async def link_client_to_book(client_id: int, book_id: int, token: str = Depends(verify_token)):
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
@router.delete("/clients/{client_id}/return-book/{book_id}")
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