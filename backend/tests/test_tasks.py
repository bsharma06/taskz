"""Tests for task endpoints."""
import pytest
from datetime import datetime, timedelta, timezone
from fastapi import status


@pytest.fixture
def test_task(client, db_session, test_user, auth_headers):
    """Create a test task."""
    from uuid import uuid4
    from app.models.task import Task

    task = Task(
        id=str(uuid4()),
        title="Test Task",
        description="Test Description",
        start_date=datetime.now(timezone.utc),
        due_date=datetime.now(timezone.utc) + timedelta(days=7),
        priority="high",
        status="pending",
        created_by=test_user.user_email.lower(),
        assigned_to=test_user.user_email.lower()
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task


def test_create_task(client, test_user, auth_headers):
    """Test creating a new task."""
    start_date = datetime.now(timezone.utc)
    due_date = start_date + timedelta(days=7)

    response = client.post(
        "/tasks/",
        json={
            "title": "New Task",
            "description": "Task Description",
            "start_date": start_date.isoformat(),
            "due_date": due_date.isoformat(),
            "priority": "medium",
            "status": "pending",
            "created_by": test_user.user_email,
            "assigned_to": test_user.user_email
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "New Task"
    assert data["assigned_to"] == test_user.user_email.lower()
    assert data["created_by"] == test_user.user_email.lower()
    assert "id" in data


def test_create_task_unauthorized(client, test_user):
    """Test creating task without authentication."""
    start_date = datetime.now(timezone.utc)
    due_date = start_date + timedelta(days=7)

    response = client.post(
        "/tasks/",
        json={
            "title": "New Task",
            "description": "Task Description",
            "start_date": start_date.isoformat(),
            "due_date": due_date.isoformat(),
            "priority": "medium",
            "status": "pending",
            "created_by": test_user.user_email,
            "assigned_to": test_user.user_email
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED




def test_list_tasks(client, test_task, test_user, auth_headers):
    """Test listing tasks - normal user sees only their tasks."""
    response = client.get("/tasks/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    task_ids = [t["id"] for t in data]
    assert test_task.id in task_ids
    # Verify all tasks are created by the current user
    for task in data:
        assert task["created_by"] == test_user.user_email.lower()


def test_list_tasks_unauthorized(client):
    """Test listing tasks without authentication."""
    response = client.get("/tasks/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_task(client, test_task, auth_headers):
    """Test getting a specific task - normal user can see their own task."""
    response = client.get(f"/tasks/{test_task.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_task.id
    assert data["title"] == test_task.title


def test_get_task_not_found(client, auth_headers):
    """Test getting a non-existent task."""
    response = client.get("/tasks/nonexistent-id", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_task(client, test_task, test_user2, auth_headers):
    """Test updating a task."""
    new_due_date = datetime.now(timezone.utc) + timedelta(days=14)

    response = client.put(
        f"/tasks/{test_task.id}",
        json={
            "title": "Updated Task",
            "status": "in_progress",
            "due_date": new_due_date.isoformat(),
            "assigned_to": test_user2.user_email
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["status"] == "in_progress"
    assert data["assigned_to"] == test_user2.user_email.lower()


def test_update_task_partial(client, test_task, auth_headers):
    """Test partial update of a task."""
    response = client.put(
        f"/tasks/{test_task.id}",
        json={"status": "completed"},
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "completed"
    assert data["title"] == test_task.title  # Other fields unchanged




def test_delete_task(client, test_task, auth_headers):
    """Test deleting a task."""
    response = client.delete(f"/tasks/{test_task.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify task is deleted
    get_response = client.get(f"/tasks/{test_task.id}", headers=auth_headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_task_unauthorized(client, test_task):
    """Test deleting task without authentication."""
    response = client.delete(f"/tasks/{test_task.id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_admin_can_see_all_tasks(client, test_task, test_user2, admin_auth_headers, db_session):
    """Test that admin can see all tasks."""
    from uuid import uuid4
    from app.models.task import Task
    from datetime import datetime, timedelta, timezone
    
    # Create a task by another user
    other_task = Task(
        id=str(uuid4()),
        title="Other User Task",
        description="Task by another user",
        start_date=datetime.now(timezone.utc),
        due_date=datetime.now(timezone.utc) + timedelta(days=7),
        priority="low",
        status="pending",
        created_by=test_user2.user_email.lower(),
        assigned_to=test_user2.user_email.lower()
    )
    db_session.add(other_task)
    db_session.commit()
    
    # Admin should see both tasks
    response = client.get("/tasks/", headers=admin_auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 2
    task_ids = [t["id"] for t in data]
    assert test_task.id in task_ids
    assert other_task.id in task_ids


def test_normal_user_cannot_see_other_tasks(client, test_task, test_user2, auth_headers, db_session):
    """Test that normal user cannot see tasks created by others."""
    from uuid import uuid4
    from app.models.task import Task
    from datetime import datetime, timedelta, timezone
    
    # Create a task by another user
    other_task = Task(
        id=str(uuid4()),
        title="Other User Task",
        description="Task by another user",
        start_date=datetime.now(timezone.utc),
        due_date=datetime.now(timezone.utc) + timedelta(days=7),
        priority="low",
        status="pending",
        created_by=test_user2.user_email.lower(),
        assigned_to=test_user2.user_email.lower()
    )
    db_session.add(other_task)
    db_session.commit()
    
    # Normal user should only see their own task
    response = client.get("/tasks/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    task_ids = [t["id"] for t in data]
    assert test_task.id in task_ids
    assert other_task.id not in task_ids


def test_normal_user_cannot_access_other_user_task(client, test_user2, auth_headers, db_session):
    """Test that normal user cannot access task created by another user."""
    from uuid import uuid4
    from app.models.task import Task
    from datetime import datetime, timedelta, timezone
    
    # Create a task by another user
    other_task = Task(
        id=str(uuid4()),
        title="Other User Task",
        description="Task by another user",
        start_date=datetime.now(timezone.utc),
        due_date=datetime.now(timezone.utc) + timedelta(days=7),
        priority="low",
        status="pending",
        created_by=test_user2.user_email.lower(),
        assigned_to=test_user2.user_email.lower()
    )
    db_session.add(other_task)
    db_session.commit()
    
    # Normal user should not be able to access this task
    response = client.get(f"/tasks/{other_task.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_admin_can_access_any_task(client, test_task, admin_auth_headers):
    """Test that admin can access any task."""
    response = client.get(f"/tasks/{test_task.id}", headers=admin_auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_task.id

