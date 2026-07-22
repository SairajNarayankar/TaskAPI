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

@app.post("/tasks", status_code=201)
def create_task(payload: TaskCreate):
    """Insert a new task. Returns 201 with the created task (including its new id)."""
    conn = database.get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            (payload.title, 0)  # done starts as 0 (false)
        )
        conn.commit()
        new_id = cursor.lastrowid  # SQLite returns the auto-assigned id

        # Fetch the row we just inserted, to return the full object
        row = conn.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (new_id,)
        ).fetchone()
        return row_to_dict(row)
    finally:
        conn.close()

@app.put("/tasks/{task_id}")
def update_task(task_id: int, payload: TaskUpdate):
    """Update a task's title and/or done status. 404 if id missing, 400 if body empty."""
    if payload.title is None and payload.done is None:
        raise HTTPException(status_code=400, detail="Body must include 'title' and/or 'done'")

    conn = database.get_connection()
    try:
        # First, check the task exists
        existing = conn.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        if existing is None:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

        # Merge new values with existing ones (partial update)
        new_title = payload.title if payload.title is not None else existing["title"]
        new_done = int(payload.done) if payload.done is not None else existing["done"]

        conn.execute(
            "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
            (new_title, new_done, task_id)
        )
        conn.commit()

        # Return the updated row
        row = conn.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        return row_to_dict(row)
    finally:
        conn.close()


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Delete a task. Returns 204 on success, 404 if not found."""
    conn = database.get_connection()
    try:
        cursor = conn.execute(
            "DELETE FROM tasks WHERE id = ?", (task_id,)
        )
        conn.commit()

        # rowcount tells us if anything was actually deleted
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

        return Response(status_code=204)
    finally:
        conn.close()