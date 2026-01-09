"""Tests for todo API endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_todo():
    """Test creating a new todo."""
    response = client.post(
        "/v1/todos",
        json={"title": "Test todo", "description": "Test description"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test todo"
    assert data["completed"] is False


def test_list_todos():
    """Test listing todos."""
    # Create a todo first
    client.post(
        "/v1/todos",
        json={"title": "List test todo"},
    )
    
    response = client.get("/v1/todos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_todo():
    """Test updating a todo."""
    # Create a todo
    create_response = client.post(
        "/v1/todos",
        json={"title": "Update test"},
    )
    todo_id = create_response.json()["id"]
    
    # Update it
    response = client.patch(
        f"/v1/todos/{todo_id}",
        json={"completed": True},
    )
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_delete_todo():
    """Test deleting a todo."""
    # Create a todo
    create_response = client.post(
        "/v1/todos",
        json={"title": "Delete test"},
    )
    todo_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/v1/todos/{todo_id}")
    assert response.status_code == 204
    
    # Verify it's gone
    get_response = client.get(f"/v1/todos/{todo_id}")
    assert get_response.status_code == 404
