import sqlite3
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

DB_PATH = os.environ.get("DB_PATH", "visits.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    db_dir = os.path.dirname(DB_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS visits "
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
    )
    conn.commit()
    conn.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
def index():
    conn = get_db()
    conn.execute("INSERT INTO visits DEFAULT VALUES")
    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM visits").fetchone()[0]
    conn.close()
    plural = "s" if count != 1 else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Hello World</title>
  <style>
    body {{
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      margin: 0;
      background-color: #0069ff;
      font-family: Arial, sans-serif;
      color: #ffffff;
    }}
    h1 {{ font-size: 3rem; margin-bottom: 0.5rem; }}
    p  {{ font-size: 1.25rem; opacity: 0.85; }}
  </style>
</head>
<body>
  <h1>Hello, World!</h1>
  <p>This page has been visited <strong>{count}</strong> time{plural}.</p>
</body>
</html>"""
