"""Tests for user endpoints."""
import pytest
from fastapi import status


def test_create_user(client):
    """Test creating a new user without authentication."""
    response = client.post(
        "/users/",
        json={
            "user_email": "newuser@example.com",
            "user_name": "New User",
            "pwd": "password123"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["user_email"] == "newuser@example.com"
    assert data["user_name"] == "New User"
    assert "id" in data
    # Password should not be in response
    assert "pwd" not in data


def test_create_user_existing_requires_auth(client, test_user):
    """Test creating user with existing email requires authentication."""
    response = client.post(
        "/users/",
        json={
            "user_email": test_user.user_email,
            "user_name": "Another User",
            "pwd": "password123"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED




def test_create_user_duplicate_email_with_auth(client, test_user, auth_headers):
    """Test creating user with duplicate email when authenticated."""
    response = client.post(
        "/users/",
        json={
            "user_email": test_user.user_email,
            "user_name": "Another User",
            "pwd": "password123"
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_list_users(client, test_user, auth_headers):
    """Test listing users."""
    response = client.get("/users/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    user_emails = [u["user_email"] for u in data]
    assert test_user.user_email in user_emails


def test_list_users_unauthorized(client):
    """Test listing users without authentication."""
    response = client.get("/users/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_user(client, test_user, auth_headers):
    """Test getting a specific user."""
    response = client.get(f"/users/{test_user.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_user.id
    assert data["user_email"] == test_user.user_email




def test_update_user(client, test_user, auth_headers):
    """Test updating a user."""
    response = client.put(
        f"/users/{test_user.id}",
        json={
            "user_name": "Updated Name",
            "user_email": "updated@example.com"
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["user_name"] == "Updated Name"
    assert data["user_email"] == "updated@example.com"


def test_update_user_password(client, test_user, auth_headers):
    """Test updating user password."""
    response = client.put(
        f"/users/{test_user.id}",
        json={"pwd": "newpassword123"},
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK

    # Verify new password works
    login_response = client.post(
        "/auth/login",
        data={
            "username": test_user.user_email,
            "password": "newpassword123"
        }
    )
    assert login_response.status_code == status.HTTP_200_OK


def test_delete_user(client, test_user2, auth_headers):
    """Test deleting a user."""
    response = client.delete(f"/users/{test_user2.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify user is deleted
    get_response = client.get(f"/users/{test_user2.id}", headers=auth_headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

