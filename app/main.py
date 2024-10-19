from fastapi import FastAPI
from app.routers import books, authors, genres, publishers, borrowers, borrowing_history
from db.engine import engine
from db.models import Base

# Create the database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# ------------------------------------
# Include Routers
# ------------------------------------

app.include_router(books.router)
app.include_router(authors.router)
app.include_router(genres.router)
app.include_router(publishers.router)
app.include_router(borrowers.router)
app.include_router(borrowing_history.router)

# ------------------------------------
# Root Endpoint
# ------------------------------------

@app.get("/")
async def read_root() -> dict:
    """Root endpoint."""
    return {"message": "Welcome to the Library Management System API!"}
