from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from . import database, models, security
from .config import SECRET_KEY, ALGORITHM
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # You'll create a /token endpoint

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

async def get_optional_current_user(token: Optional[str] = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    try:
        return await get_current_user(token, db)
    except HTTPException as e:
        if e.status_code == status.HTTP_401_UNAUTHORIZED:
            return None # User is not authenticated, but that's okay
        raise e # Re-raise other HTTP exceptions
