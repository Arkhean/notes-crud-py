from fastapi import APIRouter, Response, Depends, Path

from app.db import get_db
from app.schema import (
    NoteListSerializer,
    NoteSerializer,
    NoteCreateValidator,
    NoteUpdateValidator,
    NoteSearchFilter,
)
from app.services import NoteService

router = APIRouter(prefix="/notes")


@router.post("/search", description="Search Notes.", response_model=NoteListSerializer)
def search(data: NoteSearchFilter, db=Depends(get_db)):
    count, records = NoteService.search(db=db, **data.model_dump())
    return {"count": count, "notes": records}


@router.get(
    "/{noteId}", description="Get a note by its ID.", response_model=NoteSerializer
)
def get_by_id(note_id: int = Path(alias="noteId"), db=Depends(get_db)):
    record = NoteService.get(db=db, pk=note_id)
    return NoteService.to_schema(record)


@router.post(
    "", description="Create a new note.", response_model=NoteSerializer, status_code=201
)
def create(data: NoteCreateValidator, db=Depends(get_db)):
    record = NoteService.create(db=db, **data.model_dump())
    return NoteService.to_schema(record)


@router.patch(
    "/{noteId}", description="Update an existing note.", response_model=NoteSerializer
)
def update(
    data: NoteUpdateValidator, note_id: int = Path(alias="noteId"), db=Depends(get_db)
):
    # get note (check 404)
    record = NoteService.get(db=db, pk=note_id)
    # update the note
    record = NoteService.update(record=record, **data.model_dump())
    return NoteService.to_schema(record)


@router.delete("/{noteId}", description="Delete a note.", status_code=204)
def delete(note_id: int = Path(alias="noteId"), db=Depends(get_db)):
    # get note (check 404)
    record = NoteService.get(db=db, pk=note_id)
    # delete note
    NoteService.delete(db=db, record=record)
    # return empty response
    return Response(status_code=204)
