"""Tests for user endpoints."""
import pytest
from fastapi import status


def test_create_user(client):
    """Test creating a new user without authentication."""
    response = client.post(
        "/users/",
        json={
            "user_email": "NewUser@Example.com",
            "user_name": "New User",
            "pwd": "password123"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    # Email should be saved in lowercase
    assert data["user_email"] == "newuser@example.com"
    assert data["user_name"] == "New User"
    assert data["role"] == "normal"  # Default role
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
    """Test listing users - normal user sees only themselves."""
    response = client.get("/users/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1  # Normal user should only see themselves
    assert data[0]["id"] == test_user.id
    assert data[0]["user_email"] == test_user.user_email


def test_list_users_unauthorized(client):
    """Test listing users without authentication."""
    response = client.get("/users/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_user(client, test_user, auth_headers):
    """Test getting a specific user - normal user can see themselves."""
    response = client.get(f"/users/{test_user.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_user.id
    assert data["user_email"] == test_user.user_email


def test_normal_user_cannot_see_other_user(client, test_user2, auth_headers):
    """Test that normal user cannot see other users."""
    response = client.get(f"/users/{test_user2.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_admin_can_see_all_users(client, test_user, test_user2, admin_auth_headers):
    """Test that admin can see all users."""
    response = client.get("/users/", headers=admin_auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    user_ids = [u["id"] for u in data]
    assert test_user.id in user_ids
    assert test_user2.id in user_ids


def test_admin_can_see_any_user(client, test_user, admin_auth_headers):
    """Test that admin can see any user."""
    response = client.get(f"/users/{test_user.id}", headers=admin_auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_user.id




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

