# ⛏️ Course Material Aggregator
### A modular "redstone contraption" built with FastAPI + SQLite + Tailwind

This project scrapes free OpenStax textbooks, stores them in a local SQLite
database, serves them through a small FastAPI API, and displays them in a
dark-mode web UI.

---

## 🧱 Components ("Redstone" Parts)

| File              | Role                    | Description                                              |
|-------------------|-------------------------|-----------------------------------------------------------|
| `scraper.py`      | The Resource Farmer     | Scrapes OpenStax subject pages into `database.db`         |
| `main.py`         | The Command Block       | FastAPI server exposing `/search` and `/subjects`         |
| `index.html`      | The Player Interface    | Dark-mode Tailwind UI that calls the API via `fetch()`     |
| `start.bat`       | The Lever                | One-click launcher (Windows)                              |
| `requirements.txt`| The Crafting Recipe     | Python dependencies                                        |
| `.venv/`          | The Crafting Table       | Isolated Python environment (don't commit this!)          |

---

## 🚀 Setup (Windows)

### 1. Create the virtual environment
```bat
py -m venv .venv
```

### 2. Install dependencies (using the .venv's pip!)
```bat
.venv\Scripts\pip install -r requirements.txt
```

### 3. Run the scraper to harvest textbooks
```bat
.venv\Scripts\python scraper.py
```
This creates/fills `database.db`. It waits 2 seconds between requests to be
server-friendly to OpenStax.

> **Note:** If the scraper reports 0 results for a subject, OpenStax may have
> changed their page layout. Open the page in a browser, inspect the HTML,
> and adjust the parsing logic in `scrape_subject_page()` inside `scraper.py`.

### 4. Launch everything
```bat
start.bat
```
This activates `.venv`, starts the FastAPI server at
`http://127.0.0.1:8000`, waits 3 seconds, and opens `index.html` in your
browser.

---

## 🔌 API Reference

| Endpoint    | Method | Description                                  |
|-------------|--------|-----------------------------------------------|
| `/`         | GET    | Health check                                  |
| `/search`   | GET    | `?q=<term>&subject=<subject>&limit=<n>`       |
| `/subjects` | GET    | List of all distinct subjects in the database |

Example:
```
http://127.0.0.1:8000/search?q=biology
```

---

## 🛡️ Error Handling

- All database calls are wrapped in `try/except` and return friendly JSON
  error messages (e.g. *"Database not ready - run scraper.py first"*)
  instead of stack traces.
- All web requests in `scraper.py` are wrapped in `try/except` and will skip
  a page gracefully if it can't be reached.
- The UI shows an "API Offline" badge and a friendly empty-state message if
  it can't reach the server.

---

## 🧪 Troubleshooting

- **"API Offline" in the UI** → Make sure the server window opened by
  `start.bat` is still running. Give it a few seconds and refresh.
- **0 results everywhere** → Run `scraper.py` first; `database.db` doesn't
  exist until it's run at least once.
- **`'py' is not recognized`** → Install Python from python.org and make sure
  "Add Python to PATH" was checked during install.