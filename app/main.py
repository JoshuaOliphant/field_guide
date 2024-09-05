from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Templates
templates = Jinja2Templates(directory="app/templates")

# Import routers
from app.routers import notes, pages

# Include routers
app.include_router(notes.router, prefix="/notes")
app.include_router(pages.router)

# Make templates available to routers
app.state.templates = templates

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
