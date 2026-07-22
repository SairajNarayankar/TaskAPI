from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field
from typing import Optional
import database  # runs init_db()

app = FastAPI(title="Task API", version="2.0")


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    done: Optional[bool] = None


def row_to_dict(row) -> dict:
    """Convert a sqlite3.Row into a dict with proper boolean for done."""
    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])  # SQLite stores 0/1, API returns true/false
    }


@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "2.0",
        "storage": "SQLite (tasks.db)",
        "endpoints": ["/tasks", "/tasks/{id}", "/health"]
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    """Return all tasks from the database."""
    conn = database.get_connection()
    try:
        rows = conn.execute("SELECT * FROM tasks").fetchall()
        return [row_to_dict(r) for r in rows]
    finally:
        conn.close()


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Return one task by id. 404 if not found."""
    conn = database.get_connection()
    try:
        # Parameterized query — the ? placeholder keeps user input safe
        row = conn.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        return row_to_dict(row)
    finally:
        conn.close()