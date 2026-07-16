from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Task API", version="1.0")

tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": True},
    {"id": 2, "title": "Build CRUD API", "done": False},
    {"id": 3, "title": "Push to GitHub", "done": False},
]


# Pydantic model for input validation
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, description="Task title (required, non-empty)")


@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks", "/tasks/{id}", "/health"]
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.post("/tasks", status_code=201)
def create_task(payload: TaskCreate):
    """Create a new task. Returns 201 with the created task."""
    # Compute next free id
    next_id = max((t["id"] for t in tasks), default=0) + 1
    new_task = {
        "id": next_id,
        "title": payload.title,
        "done": False
    }
    tasks.append(new_task)
    return new_task