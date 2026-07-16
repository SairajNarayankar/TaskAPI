from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="Task API", version="1.0")

tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": True},
    {"id": 2, "title": "Build CRUD API", "done": False},
    {"id": 3, "title": "Push to GitHub", "done": False},
]


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    done: Optional[bool] = None


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
    next_id = max((t["id"] for t in tasks), default=0) + 1
    new_task = {"id": next_id, "title": payload.title, "done": False}
    tasks.append(new_task)
    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, payload: TaskUpdate):
    """Update a task's title and/or done status."""
    # Must send at least one field
    if payload.title is None and payload.done is None:
        raise HTTPException(status_code=400, detail="Body must include 'title' and/or 'done'")

    for task in tasks:
        if task["id"] == task_id:
            if payload.title is not None:
                task["title"] = payload.title
            if payload.done is not None:
                task["done"] = payload.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Delete a task. Returns 204 (no content) on success."""
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")