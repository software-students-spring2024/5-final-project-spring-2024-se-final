"""
This module initializes the pytest test cases for app.py web app.
"""

from unittest.mock import MagicMock
import pytest
from bson import ObjectId
from app import app, projects_collection, characters_collection, locations_collection

# pylint: disable=redefined-outer-name
# pylint: disable=no-member


@pytest.fixture
def client():
    """Create a test client for the app."""
    with app.test_client() as client:
        yield client


def test_home_route(client):
    """Test the home route."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"World-Build Manager" in response.data


def test_create_project(client, mocker):
    """Test creating a new project."""
    data = {"title": "Test Project", "description": "Test Description"}
    mocker.patch(
        "app.projects_collection.insert_one", return_value=MagicMock(inserted_id="123")
    )
    response = client.post("/projects", json=data)
    assert response.status_code == 201
    assert b"project_id" in response.data


def test_get_projects(client, mocker):
    """Test getting all projects."""
    mocker.patch(
        "app.projects_collection.find",
        return_value=[
            {"_id": "123", "title": "Project 1", "description": "Description 1"},
            {"_id": "456", "title": "Project 2", "description": "Description 2"},
        ],
    )
    response = client.get("/projects")
    assert response.status_code == 200
    assert b"Project 1" in response.data
    assert b"Project 2" in response.data


def test_project_details(client, mocker):
    """Test rendering project details."""
    mocker.patch(
        "app.projects_collection.find_one",
        return_value={
            "_id": ObjectId("606ab6e7f1e87c8502e1834f"),
            "title": "Project 1",
        },
    )
    mocker.patch(
        "app.characters_collection.find",
        return_value=[
            {"_id": ObjectId("606ab6e7f1e87c8502e18350"), "name": "Character 1"},
            {"_id": ObjectId("606ab6e7f1e87c8502e18351"), "name": "Character 2"},
        ],
    )
    mocker.patch(
        "app.locations_collection.find",
        return_value=[
            {"_id": ObjectId("606ab6e7f1e87c8502e18352"), "name": "Location 1"},
            {"_id": ObjectId("606ab6e7f1e87c8502e18353"), "name": "Location 2"},
        ],
    )
    response = client.get("/projects/606ab6e7f1e87c8502e1834f")
    assert response.status_code == 200
    assert b"Project 1" in response.data
    assert b"Character 1" in response.data
    assert b"Character 2" in response.data
    assert b"Location 1" in response.data
    assert b"Location 2" in response.data


def test_update_project(client, mocker):
    """Test updating project data."""
    data = {"title": "Updated Project", "description": "Updated Description"}
    project_id = "606ab6e7f1e87c8502e1834f"
    mocker.patch("app.projects_collection.update_one")
    response = client.post(f"/projects/{project_id}", data=data)
    assert response.status_code == 302
    projects_collection.update_one.assert_called_once_with(
        {"_id": ObjectId(project_id)}, {"$set": data}
    )


def test_delete_project(client, mocker):
    """Test deleting a project."""
    project_id = "606ab6e7f1e87c8502e1834f"
    mocker.patch("app.projects_collection.delete_one")
    response = client.post(f"/projects/{project_id}/delete")
    assert response.status_code == 302
    projects_collection.delete_one.assert_called_once_with(
        {"_id": ObjectId(project_id)}
    )


def test_add_character(client, mocker):
    """Test adding a character to a project."""
    data = {"name": "New Character", "description": "Character Description"}
    project_id = "606ab6e7f1e87c8502e1834f"
    mocker.patch.object(characters_collection, "insert_one")
    response = client.post(f"/projects/{project_id}/characters", data=data)
    assert response.status_code == 302
    expected_data = {
        "name": "New Character",
        "description": "Character Description",
        "project_id": project_id,
    }
    characters_collection.insert_one.assert_called_once_with(expected_data)


def test_add_location(client, mocker):
    """Test adding a location to a project."""
    data = {"name": "New Location", "description": "Location Description"}
    project_id = "606ab6e7f1e87c8502e1834f"
    mocker.patch.object(locations_collection, "insert_one")
    response = client.post(f"/projects/{project_id}/locations", data=data)
    assert response.status_code == 302
    expected_data = {
        "name": "New Location",
        "description": "Location Description",
        "project_id": project_id,
    }
    locations_collection.insert_one.assert_called_once_with(expected_data)
