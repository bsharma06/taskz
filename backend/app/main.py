# uvicorn app.main:app --reload

from fastapi import FastAPI
from app.api.routes import tasks, users, auth

app = FastAPI(title="taskz")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])


@app.get("/")
def read_root():
    """Root endpoint."""
    return {"message": "Taskz API", "version": "1.0.0"}