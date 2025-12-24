from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.task import Task
from app.models.user import User
from app.schemas.task_schema import TaskCreate, TaskRead, TaskUpdate
from app.api.routes.auth import get_current_user, get_current_user_tenant_id
from typing import List, Optional

router = APIRouter()


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[TaskRead])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: Optional[str] = Depends(get_current_user_tenant_id)
):
    """List all tasks for the current user's tenant."""
    tasks = db.query(Task).filter(Task.tenant_id == tenant_id).all()
    return tasks


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def add_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: Optional[str] = Depends(get_current_user_tenant_id)
):
    """Create a new task."""
    # Verify assigned user exists and belongs to the same tenant
    assigned_user = db.query(User).filter(
        User.id == task_in.assigned_to,
        User.tenant_id == tenant_id
    ).first()
    if not assigned_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assigned user not found or does not belong to your tenant"
        )

    new_task = Task(
        id=str(uuid4()),
        title=task_in.title,
        description=task_in.description,
        start_date=task_in.start_date,
        due_date=task_in.due_date,
        priority=task_in.priority,
        status=task_in.status,
        assigned_to=task_in.assigned_to,
        tenant_id=tenant_id,
    )

    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}"
        )


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: Optional[str] = Depends(get_current_user_tenant_id)
):
    """Get a task by ID (only if it belongs to user's tenant)."""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.tenant_id == tenant_id
    ).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: str,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: Optional[str] = Depends(get_current_user_tenant_id)
):
    """Update a task (only if it belongs to user's tenant)."""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.tenant_id == tenant_id
    ).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # If assigned_to is being updated, verify the user exists and belongs to tenant
    if task_in.assigned_to is not None:
        assigned_user = db.query(User).filter(
            User.id == task_in.assigned_to,
            User.tenant_id == tenant_id
        ).first()
        if not assigned_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assigned user not found or does not belong to your tenant"
            )
        task.assigned_to = task_in.assigned_to

    if task_in.title is not None:
        task.title = task_in.title
    if task_in.description is not None:
        task.description = task_in.description
    if task_in.start_date is not None:
        task.start_date = task_in.start_date
    if task_in.due_date is not None:
        task.due_date = task_in.due_date
    if task_in.priority is not None:
        task.priority = task_in.priority
    if task_in.status is not None:
        task.status = task_in.status

    try:
        db.commit()
        db.refresh(task)
        return task
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating task: {str(e)}"
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: Optional[str] = Depends(get_current_user_tenant_id)
):
    """Delete a task (only if it belongs to user's tenant)."""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.tenant_id == tenant_id
    ).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    try:
        db.delete(task)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting task: {str(e)}"
        )