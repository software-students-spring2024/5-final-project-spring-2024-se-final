"""
This module initializes the main Flask web app.
"""

from flask import Flask, request, jsonify, render_template, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

app = Flask(__name__, template_folder="templates")

# Connect to MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["WBM"]
projects_collection = db["projects"]
characters_collection = db["characters"]
locations_collection = db["locations"]

# Define routes and other Flask application logic below
@app.route("/")
def home():
    """Renders the default index.html home page."""
    return render_template("index.html")

# Create a new project
@app.route("/projects", methods=["POST"])
def create_project():
    data = request.json
    project_id = projects_collection.insert_one(data).inserted_id
    return jsonify({"project_id": str(project_id)}), 201

# Read existing projects
@app.route("/projects", methods=["GET"])
def get_projects():
    projects = list(projects_collection.find())
    for project in projects:
        project['_id'] = str(project['_id'])
    return jsonify(projects)

# Route for project details page
@app.route("/projects/<project_id>")
def project_details(project_id):
    project = projects_collection.find_one({"_id": ObjectId(project_id)})
    characters = list(characters_collection.find({"project_id": project_id}))
    locations = list(locations_collection.find({"project_id": project_id}))
    return render_template("project_details.html", project=project, characters=characters, locations=locations)

# Route for updating project data
@app.route("/projects/<project_id>", methods=["POST"])
def update_project(project_id):
    data = request.form.to_dict()  # Access form data
    projects_collection.update_one(
        {"_id": ObjectId(project_id)},
        {"$set": data}
    )
    return redirect(url_for('project_details', project_id=project_id))

# Route for deleting a project
@app.route("/projects/<project_id>/delete", methods=["POST"])
def delete_project(project_id):
    projects_collection.delete_one({"_id": ObjectId(project_id)})
    return redirect(url_for('home'))

# Route for adding characters to a project
@app.route("/projects/<project_id>/characters", methods=["POST"])
def add_character(project_id):
    data = request.form.to_dict()  # Access form data
    data["project_id"] = project_id
    character_id = characters_collection.insert_one(data).inserted_id
    # Redirect the user back to the project details page
    return redirect(url_for('project_details', project_id=project_id))

# Route for adding locations to a project
@app.route("/projects/<project_id>/locations", methods=["POST"])
def add_location(project_id):
    data = request.form.to_dict()  # Access form data
    data["project_id"] = project_id
    location_id = locations_collection.insert_one(data).inserted_id
    # Redirect the user back to the project details page
    return redirect(url_for('project_details', project_id=project_id))

# Route for updating character data
@app.route("/projects/<project_id>/characters/<character_id>", methods=["POST"])
def update_character(project_id, character_id):
    data = request.form.to_dict()  # Access form data
    characters_collection.update_one(
        {"_id": ObjectId(character_id)},
        {"$set": data}
    )
    return redirect(url_for('project_details', project_id=project_id))

# Route for updating location data
@app.route("/projects/<project_id>/locations/<location_id>", methods=["POST"])
def update_location(project_id, location_id):
    data = request.form.to_dict()  # Access form data
    locations_collection.update_one(
        {"_id": ObjectId(location_id)},
        {"$set": data}
    )
    return redirect(url_for('project_details', project_id=project_id))

# Route for rendering character details page
@app.route("/projects/<project_id>/characters/<character_id>")
def character_details(project_id, character_id):
    character = characters_collection.find_one({"_id": ObjectId(character_id)})
    return render_template("character_details.html", character=character, project_id=project_id)

# Route for rendering location details page
@app.route("/projects/<project_id>/locations/<location_id>")
def location_details(project_id, location_id):
    location = locations_collection.find_one({"_id": ObjectId(location_id)})
    return render_template("location_details.html", location=location, project_id=project_id)

# Add route for deleting characters
@app.route("/projects/<project_id>/characters/<character_id>/delete", methods=["POST"])
def delete_character(project_id, character_id):
    characters_collection.delete_one({"_id": ObjectId(character_id)})
    return redirect(url_for('project_details', project_id=project_id))

# Add route for deleting locations
@app.route("/projects/<project_id>/locations/<location_id>/delete", methods=["POST"])
def delete_location(project_id, location_id):
    locations_collection.delete_one({"_id": ObjectId(location_id)})
    return redirect(url_for('project_details', project_id=project_id))

if __name__ == "__main__":
    app.run(debug=True)
