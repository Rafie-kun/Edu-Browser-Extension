"""
main.py
-----------------------------------------------------------------------------
THE COMMAND BLOCK
-----------------------------------------------------------------------------
This is the "brain" of our redstone contraption. It's a FastAPI web server
that:
  1. Opens the SQLite "chest" (database.db).
  2. Exposes a `/search` endpoint that the Player Interface (index.html)
     can call to find textbooks by keyword/subject.
  3. Has CORS middleware enabled - this is the "portal" that lets the
     UI (running on a different origin, e.g. file:// or a different port)
     cross dimensions and talk to this API without the browser blocking it.

How it fits into the system:
  - scraper.py fills database.db with data.
  - main.py (THIS FILE) reads that data and serves it over HTTP.
  - index.html calls this API via fetch() to display results to the player.

To run manually:
  .venv\\Scripts\\python -m uvicorn main:app --reload
  (start.bat does this for you automatically)
-----------------------------------------------------------------------------
"""

import sqlite3

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

DB_PATH = "database.db"

app = FastAPI(
    title="Course Material Aggregator - Command Block",
    description="API for searching aggregated OpenStax course materials.",
    version="1.0.0",
)

# -----------------------------------------------------------------------------
# THE PORTAL (CORS Middleware)
# -----------------------------------------------------------------------------
# Without this, opening index.html directly in a browser (file://) or from
# a different local server/port would be BLOCKED by the browser's
# same-origin policy when it tries to fetch() from this API.
# allow_origins=["*"] keeps things simple for local development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------------------------------------------
# DATABASE HELPER (Reaching into the Chest)
# -----------------------------------------------------------------------------
def get_connection():
    """
    Opens a connection to database.db.
    row_factory lets us get dictionary-like rows instead of plain tuples,
    which makes it much easier to turn results into JSON.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------------------------------------------------------
# ROUTES (The Redstone Wires)
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    """
    A simple health-check route. Visit http://127.0.0.1:8000/ to confirm
    the Command Block is powered on.
    """
    return {
        "status": "online",
        "message": "Course Material Aggregator API is running.",
        "try": "/search?q=biology",
    }


@app.get("/search")
def search_books(
    q: str = Query(default="", description="Search term (matches title or subject)"),
    subject: str = Query(default="", description="Optional exact subject filter"),
    limit: int = Query(default=1000, ge=1, le=1000, description="Max results to return"),
):
    """
    The main "lever" of the contraption.

    Query Examples:
      /search?q=biology
      /search?q=intro&subject=Math
      /search?q=&subject=Science    -> all science books

    Returns a JSON list of matching books, or a friendly error message
    if something goes wrong (e.g. database missing).
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Build the query dynamically based on which filters were provided.
        sql = "SELECT id, title, subject, url, source, scraped_at FROM books WHERE 1=1"
        params = []

        if q:
            sql += " AND (title LIKE ? OR subject LIKE ?)"
            like_term = f"%{q}%"
            params.extend([like_term, like_term])

        if subject:
            sql += " AND subject = ?"
            params.append(subject)

        sql += " ORDER BY title ASC LIMIT ?"
        params.append(limit)

        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()

        results = [dict(row) for row in rows]

        return {
            "status": "ok",
            "count": len(results),
            "results": results,
        }

    except sqlite3.OperationalError:
        # Most likely cause: database.db doesn't exist yet or
        # the 'books' table hasn't been created.
        return {
            "status": "error",
            "message": (
                "The database isn't ready yet. "
                "Please run scraper.py first to harvest some textbooks!"
            ),
            "results": [],
        }
    except Exception as e:
        # Catch-all so the player NEVER sees a raw Python stack trace.
        return {
            "status": "error",
            "message": f"Something went wrong while searching: {e}",
            "results": [],
        }


@app.get("/subjects")
def list_subjects():
    """
    Returns the distinct list of subjects currently in the database.
    Useful for populating a filter dropdown in the UI.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT subject FROM books ORDER BY subject ASC")
        subjects = [row["subject"] for row in cursor.fetchall()]
        conn.close()
        return {"status": "ok", "subjects": subjects}
    except sqlite3.OperationalError:
        return {
            "status": "error",
            "message": "The database isn't ready yet. Please run scraper.py first.",
            "subjects": [],
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "subjects": []}