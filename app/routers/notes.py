from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from ..markdown_processor import get_markdown_files, process_markdown_file
import os

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

NOTES_DIR = "content/notes"


@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
async def list_notes(request: Request):
    note_files = get_markdown_files(NOTES_DIR)
    notes = [
        process_markdown_file(os.path.join(NOTES_DIR, file))
        for file in note_files
    ]
    return templates.TemplateResponse("partials/note_list.html", {
        "request": request,
        "notes": notes
    })


@router.get("/{note_slug}", response_class=HTMLResponse)
async def read_note(request: Request, note_slug: str):
    note_files = get_markdown_files(NOTES_DIR)
    for file in note_files:
        note = process_markdown_file(os.path.join(NOTES_DIR, file))
        if note['slug'] == note_slug:
            return templates.TemplateResponse("note.html", {
                "request": request,
                "note": note
            })
    raise HTTPException(status_code=404, detail="Note not found")


@router.get("/api/note-preview/{note_slug}")
async def get_note_preview(note_slug: str):
    note_files = get_markdown_files(NOTES_DIR)
    for file in note_files:
        note = process_markdown_file(os.path.join(NOTES_DIR, file))
        if note['slug'] == note_slug:
            preview = note['content'][:100] + "..." if len(
                note['content']) > 100 else note['content']
            return JSONResponse({"title": note['title'], "preview": preview})
    raise HTTPException(status_code=404, detail="Note not found")


@router.get("/content/{note_slug}", response_class=HTMLResponse)
async def get_note_content(request: Request, note_slug: str):
    note_files = get_markdown_files(NOTES_DIR)
    for file in note_files:
        note = process_markdown_file(os.path.join(NOTES_DIR, file))
        if note['slug'] == note_slug:
            return templates.TemplateResponse("partials/note_content.html", {
                "request": request,
                "note": note
            })
    raise HTTPException(status_code=404, detail="Note not found")
