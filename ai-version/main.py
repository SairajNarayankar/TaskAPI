from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(
    title="To-Do List API",
    version="1.0.0",
    description="A lightweight, in-memory FastAPI application for managing tasks."
)

# --- Pydantic Data Models ---
class Task(BaseModel):
    id: int
    title: str
    done: bool

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, description="The title cannot be empty or missing.")

class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, description="New title for the task.")
    done: bool | None = Field(None, description="Completion status of the task.")

# --- In-Memory Database Seed Data ---
tasks_db: List[dict] = [
    {"id": 1, "title": "Configure local environment", "done": True},
    {"id": 2, "title": "Deploy multi-container stack", "done": False},
    {"id": 3, "title": "Write robust API documentation", "done": False}
]
current_id = 4

# --- API Endpoints ---
@app.get("/", tags=["System"], summary="Get API Metadata")
def read_root():
    return {
        "name": app.title,
        "version": app.version,
        "endpoints": ["/", "/health", "/tasks", "/tasks/{id}"]
    }

@app.get("/health", tags=["System"], summary="API Health Check")
def health_check():
    return {"status": "ok"}

@app.get("/tasks", response_model=List[Task], tags=["Tasks"], summary="Retrieve all tasks")
def get_tasks():
    return tasks_db

@app.get("/tasks/{id}", response_model=Task, tags=["Tasks"], summary="Get a single task by ID")
def get_task(id: int):
    task = next((t for t in tasks_db if t["id"] == id), None)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {id} not found")
    return task

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, tags=["Tasks"], summary="Create a new task")
def create_task(payload: TaskCreate):
    global current_id
    new_task = {"id": current_id, "title": payload.title, "done": False}
    tasks_db.append(new_task)
    current_id += 1
    return new_task

@app.put("/tasks/{id}", response_model=Task, tags=["Tasks"], summary="Update an existing task payload")
def update_task(id: int, payload: TaskUpdate):
    task = next((t for t in tasks_db if t["id"] == id), None)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {id} not found")
    
    # Validation: reject if incoming body provides neither field
    if payload.title is None and payload.done is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request body cannot be empty. Provide 'title' or 'done'.")
    
    if payload.title is not None:
        task["title"] = payload.title
    if payload.done is not None:
        task["done"] = payload.done
        
    return task

@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"], summary="Remove a task by ID")
def delete_task(id: int):
    global tasks_db
    task = next((t for t in tasks_db if t["id"] == id), None)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {id} not found")
    
    tasks_db = [t for t in tasks_db if t["id"] != id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)


