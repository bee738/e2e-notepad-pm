from fastapi import APIRouter, Depends, HTTPException, status, Response, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from . import database, models, security
from . import auth as auth_utils
from . import schemas  # You'll need to create schemas.py
from .database import get_db

router = APIRouter()

# User Registration
@router.post("/register/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Login (Token generation)
@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_utils.create_access_token(subject=user.username)
    return {"access_token": access_token, "token_type": "bearer"}

# Get current user (protected endpoint example)
@router.get("/users/me/", response_model=schemas.UserRead)
async def read_users_me(current_user: models.User = Depends(auth_utils.get_current_user)):
    return current_user

# Notes API
@router.post("/notes/", response_model=schemas.NoteRead, status_code=status.HTTP_201_CREATED)
async def create_note(note: schemas.NoteCreate, current_user: models.User = Depends(auth_utils.get_current_user), db: Session = Depends(get_db)):
    db_note = models.Note(**note.dict(), owner_id=current_user.id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/notes/", response_model=List[schemas.NoteRead])
async def read_notes(skip: int = 0, limit: int = 100, current_user: models.User = Depends(auth_utils.get_current_user), db: Session = Depends(get_db)):
    notes = db.query(models.Note).filter(models.Note.owner_id == current_user.id).offset(skip).limit(limit).all()
    return notes

@router.get("/notes/{note_id}/", response_model=schemas.NoteRead)
async def read_note(note_id: int, current_user: models.User = Depends(auth_utils.get_current_user), db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note

@router.put("/notes/{note_id}/", response_model=schemas.NoteRead)
async def update_note(note_id: int, note_update: schemas.NoteUpdate, current_user: models.User = Depends(auth_utils.get_current_user), db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == current_user.id).first()
    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    for key, value in note_update.dict(exclude_unset=True).items():
        setattr(db_note, key, value)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.delete("/notes/{note_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int, current_user: models.User = Depends(auth_utils.get_current_user), db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.owner_id == current_user.id)
    if not note.first(): # Check if note exists before deleting
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    note.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Password Entries API (similar structure to Notes, but add relevant fields)
@router.post("/passwords/", response_model=schemas.PasswordEntryRead, status_code=status.HTTP_201_CREATED)
async def create_password_entry(password_entry: schemas.PasswordEntryCreate, current_user: models.User = Depends(auth_utils.get_current_user), db: Session = Depends(get_db)):
    db_password_entry = models.PasswordEntry(**password_entry.dict(), owner_id=current_user.id)
    db.add(db_password_entry)
    db.commit()
    db.refresh(db_password_entry)
    return db_password_entry

@router.get("/passwords/", response_model=List[schemas.PasswordEntryRead])
async def read_password_entries(skip: int = 0, limit: int = 100, current_user: models.User = Depends(auth_utils.get_current_user), db: Session = Depends(get_db)):
    password_entries = db.query(models.PasswordEntry).filter(models.PasswordEntry.owner_id == current_user.id).offset(skip).limit(limit).all()
    return password_entries

@router.get("/passwords/{password_id}/", response_model=schemas.PasswordEntryRead)
async def read_password_entry(password_id: int, current_user: models.User = Depends(auth_utils.get_current_user), db: Session = Depends(get_db)):
    password_entry = db.query(models.PasswordEntry).filter(models.PasswordEntry.id == password_id, models.PasswordEntry.owner_id == current_user.id).first()
    if not password_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Password entry not found")
    return password_entry

@router.put("/passwords/{password_id}/", response_model=schemas.PasswordEntryRead)
async def update_password_entry(password_id: int, password_entry_update: schemas.PasswordEntryUpdate, current_user: models.User = Depends(auth_utils.get_current_user), db: Session = Depends(get_db)):
    db_password_entry = db.query(models.PasswordEntry).filter(models.PasswordEntry.id == password_id, models.PasswordEntry.owner_id == current_user.id).first()
    if not db_password_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Password entry not found")
    for key, value in password_entry_update.dict(exclude_unset=True).items():
        setattr(db_password_entry, key, value)
    db.commit()
    db.refresh(db_password_entry)
    return db_password_entry

@router.delete("/passwords/{password_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_password_entry(password_id: int, current_user: models.User = Depends(auth_utils.get_current_user), db: Session = Depends(get_db)):
    password_entry = db.query(models.PasswordEntry).filter(models.PasswordEntry.id == password_id, models.PasswordEntry.owner_id == current_user.id)
    if not password_entry.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Password entry not found")
    password_entry.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
