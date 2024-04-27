import pytest
import json
from app import app
import pytest

@pytest.fixture
def client():
    """Create a test client for the app."""
    with app.test_client() as client:
        yield client

def test_home_route(client):
    """Test the home route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"World-Build Manager" in response.data

def test_create_project(client):
    """Test creating a new project."""
    data = {"title": "Test Project", "description": "Test Description"}
    response = client.post('/projects', json=data)
    assert response.status_code == 201
    assert b"project_id" in response.data

def test_get_projects(client):
    """Test getting existing projects."""
    response = client.get('/projects')
    assert response.status_code == 200
    assert b"Test Project" in response.data

def test_project_details(client):
    """Test rendering project details."""
    # First, create a new project
    data = {"title": "Test Project", "description": "Test Description"}
    response = client.post('/projects', json=data)
    assert response.status_code == 201
    project_id = json.loads(response.data)["project_id"]

    # Then, test accessing project details page
    response = client.get(f'/projects/{project_id}')
    assert response.status_code == 200
    assert b"Test Project" in response.data
    assert b"Test Description" in response.data

def test_add_character(client):
    """Test adding a character to a project."""
    # First, create a new project
    data = {"title": "Test Project", "description": "Test Description"}
    response = client.post('/projects', json=data)
    assert response.status_code == 201
    project_id = json.loads(response.data)["project_id"]

    # Then, add a character to the project
    character_data = {"name": "Test Character", "description": "Test Character Description"}
    response = client.post(f'/projects/{project_id}/characters', data=character_data)
    assert response.status_code == 302  # Redirect
    assert b"Test Character" in response.data

def test_add_location(client):
    """Test adding a location to a project."""
    # First, create a new project
    data = {"title": "Test Project", "description": "Test Description"}
    response = client.post('/projects', json=data)
    assert response.status_code == 201
    project_id = json.loads(response.data)["project_id"]

    # Then, add a location to the project
    location_data = {"name": "Test Location", "description": "Test Location Description"}
    response = client.post(f'/projects/{project_id}/locations', data=location_data)
    assert response.status_code == 302  # Redirect
    assert b"Test Location" in response.data
