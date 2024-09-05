from pydantic import BaseModel
from typing import List, Optional


class NoteBase(BaseModel):
    title: str
    content: str
    tags: List[str] = []


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None


class Note(NoteBase):
    id: int

    class Config:
        orm_mode = True
