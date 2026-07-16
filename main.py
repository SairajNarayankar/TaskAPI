from fastapi import FastAPI

app = FastAPI(title="Task API", version="1.0")

@app.get("/")
def root():
    """API description and available endpoints."""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks", "/tasks/{id}", "/health"]
    }

@app.get("/health")
def health():
    """Liveness check. Used by monitoring systems to verify the server is alive."""
    return {"status": "ok"}