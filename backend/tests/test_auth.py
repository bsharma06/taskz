"""Tests for authentication endpoints."""
import pytest
from fastapi import status


def test_login_success(client, test_user):
    """Test successful login."""
    response = client.post(
        "/auth/login",
        data={
            "username": test_user.user_email,
            "password": "testpassword123"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_email(client, test_user):
    """Test login with invalid email."""
    response = client.post(
        "/auth/login",
        data={
            "username": "wrong@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_invalid_password(client, test_user):
    """Test login with invalid password."""
    response = client.post(
        "/auth/login",
        data={
            "username": test_user.user_email,
            "password": "wrongpassword"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user(client, auth_headers, test_user):
    """Test getting current user info."""
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_user.id
    assert data["user_email"] == test_user.user_email
    assert data["user_name"] == test_user.user_name
    assert data["tenant_id"] == test_user.tenant_id


def test_get_current_user_no_token(client):
    """Test getting current user without token."""
    response = client.get("/auth/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user_invalid_token(client):
    """Test getting current user with invalid token."""
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

