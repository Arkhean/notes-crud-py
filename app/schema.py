from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class NoteCreateValidator(BaseModel):
    text: str


class NoteUpdateValidator(BaseModel):
    text: str


class NoteSerializer(BaseModel):
    id: int
    text: str
    created_at: datetime = Field(alias="createdAt")


class NoteListSerializer(BaseModel):
    notes: List[NoteSerializer]
    count: int


class NoteSearchFilter(BaseModel):
    text: Optional[str] = None
    limit: int = 10
    offset: int = 0
