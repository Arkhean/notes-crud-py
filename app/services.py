from typing import Sequence, Optional, Tuple

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.db import Note


class NoteService:

    @classmethod
    def search(
        cls, db: Session, text: Optional[str], limit: int, offset: int
    ) -> Tuple[int, Sequence[Note]]:
        """
        Search Notes based on filter 'text' and limit/offset. Also return total count in DB.

        :param db: database session
        :param text: find notes containing this text (case-insensitive)
        :param limit: maximum number of notes to return
        :param offset: number of notes to skip
        :return: total count and list of notes matching the filter.
        """
        query = select(Note)
        if text is not None:
            query = query.where(Note.text.ilike(f"%{text}%"))
        count = db.scalar(query.with_only_columns(func.count(Note.id)))
        query = query.limit(limit).offset(offset)
        return count, db.scalars(query).all()

    @classmethod
    def get(cls, db: Session, pk: int) -> Optional[Note]:
        """
        Get a note by its ID, raise 404 if not found.

        :param db: database session
        :param pk: note ID
        :return: the note object if found, else raise 404
        """
        query = select(Note).where(Note.id == pk)
        record = db.scalar(query)
        if record is None:
            raise HTTPException(status_code=404, detail="Note not found!")
        return record

    @classmethod
    def create(cls, db: Session, text: str) -> Note:
        """
        Insert a new note in database.

        :param db: database session
        :param text: the text of the note
        :return: the created note object.
        """
        record = Note(text=text)
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @classmethod
    def update(cls, db: Session, record: Note, text: str) -> Note:
        """
        Update record in database with new text.

        :param db: database session
        :param record: the record to update
        :param text: the new text
        :return: the updated record
        """
        record.text = text
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @classmethod
    def delete(cls, db: Session, record: Note) -> None:
        """
        Delete record from database.

        :param db: database session
        :param record: record to be deleted
        """
        db.delete(record)

    @classmethod
    def to_schema(cls, record: Note) -> dict:
        """
        Transform a note record to a dict for pydantic model.

        :param record: record to transform
        :return: a dict representing the record in schema for pydantic
        """
        return {
            "id": record.id,
            "text": record.text,
            "createdAt": record.created_at,
            "updatedAt": record.updated_at,
        }
