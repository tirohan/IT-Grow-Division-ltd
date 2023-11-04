from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException

security = OAuth2PasswordBearer(tokenUrl="token")
ALGORITHM = "HS256"
import secrets

SECRET_KEY = secrets.token_urlsafe(32)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Token expires in 15 minutes
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def does_author_exist(author_id: int, db):
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