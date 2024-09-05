from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from ..markdown_processor import process_markdown_file, get_markdown_files
import os

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

NOTES_DIR = "content/notes"
PAGES_DIR = "content/pages"


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Get recent notes
    note_files = get_markdown_files(NOTES_DIR)
    recent_notes = []
    for file in sorted(
            note_files,
            key=lambda x: os.path.getmtime(os.path.join(NOTES_DIR, x)),
            reverse=True)[:5]:
        note = process_markdown_file(os.path.join(NOTES_DIR, file))
        recent_notes.append({'title': note['title'], 'slug': note['slug']})

    return templates.TemplateResponse("index.html", {
        "request": request,
        "recent_notes": recent_notes
    })


@router.get("/{page_name}", response_class=HTMLResponse)
async def read_page(request: Request, page_name: str):
    file_path = os.path.join(PAGES_DIR, f"{page_name}.md")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Page not found")
    page = process_markdown_file(file_path)
    return templates.TemplateResponse("page.html", {
        "request": request,
        "page": page
    })
