from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# User Schemas
class UserCreate(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        orm_mode = True

# Note Schemas
class NoteBase(BaseModel):
    title: str
    encrypted_content: str

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel): # For optional updates
    title: Optional[str] = None
    encrypted_content: Optional[str] = None

class NoteRead(NoteBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# PasswordEntry Schemas
class PasswordEntryBase(BaseModel):
    website_url: str
    username: str
    encrypted_password: str
    notes: Optional[str] = None

class PasswordEntryCreate(PasswordEntryBase):
    pass

class PasswordEntryUpdate(BaseModel): # For optional updates
    website_url: Optional[str] = None
    username: Optional[str] = None
    encrypted_password: Optional[str] = None
    notes: Optional[str] = None

class PasswordEntryRead(PasswordEntryBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
