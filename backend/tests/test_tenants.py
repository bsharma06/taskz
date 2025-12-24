"""Tests for tenant endpoints."""
import pytest
from fastapi import status


def test_create_tenant(client):
    """Test creating a new tenant."""
    response = client.post(
        "/tenants/",
        json={"name": "New Tenant"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "New Tenant"
    assert "id" in data


def test_create_tenant_duplicate_name(client, test_tenant):
    """Test creating tenant with duplicate name."""
    response = client.post(
        "/tenants/",
        json={"name": test_tenant.name}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_list_tenants(client, test_tenant):
    """Test listing all tenants."""
    response = client.get("/tenants/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    tenant_names = [t["name"] for t in data]
    assert test_tenant.name in tenant_names


def test_get_tenant(client, test_tenant):
    """Test getting a specific tenant."""
    response = client.get(f"/tenants/{test_tenant.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_tenant.id
    assert data["name"] == test_tenant.name


def test_get_tenant_not_found(client):
    """Test getting a non-existent tenant."""
    response = client.get("/tenants/nonexistent-id")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_tenant(client, test_tenant):
    """Test updating a tenant."""
    response = client.put(
        f"/tenants/{test_tenant.id}",
        json={"name": "Updated Tenant Name"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Tenant Name"
    assert data["id"] == test_tenant.id


def test_update_tenant_not_found(client):
    """Test updating a non-existent tenant."""
    response = client.put(
        "/tenants/nonexistent-id",
        json={"name": "Updated Name"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_tenant_duplicate_name(client, test_tenant, test_tenant2):
    """Test updating tenant with duplicate name."""
    response = client.put(
        f"/tenants/{test_tenant.id}",
        json={"name": test_tenant2.name}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_delete_tenant(client, test_tenant):
    """Test deleting a tenant."""
    response = client.delete(f"/tenants/{test_tenant.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify tenant is deleted
    get_response = client.get(f"/tenants/{test_tenant.id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_tenant_not_found(client):
    """Test deleting a non-existent tenant."""
    response = client.delete("/tenants/nonexistent-id")
    assert response.status_code == status.HTTP_404_NOT_FOUND

