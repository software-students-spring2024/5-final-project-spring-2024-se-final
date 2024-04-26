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

# Route for adding characters to a project
@app.route("/projects/<project_id>/characters", methods=["POST"])
def add_character(project_id):
    data = request.json
    data["project_id"] = project_id
    character_id = characters_collection.insert_one(data).inserted_id
    return jsonify({"character_id": str(character_id)}), 201

# Route for adding locations to a project
@app.route("/projects/<project_id>/locations", methods=["POST"])
def add_location(project_id):
    data = request.json
    data["project_id"] = project_id
    location_id = locations_collection.insert_one(data).inserted_id
    return jsonify({"location_id": str(location_id)}), 201

# Route for deleting a project
@app.route("/projects/<project_id>", methods=["POST"])
def delete_project(project_id):
    projects_collection.delete_one({"_id": ObjectId(project_id)})
    return redirect(url_for('home'))

# Route for updating character data
@app.route("/projects/<project_id>/characters/<character_id>", methods=["PUT"])
def update_character(project_id, character_id):
    data = request.json
    characters_collection.update_one(
        {"_id": ObjectId(character_id)},
        {"$set": data}
    )
    return jsonify({"message": "Character updated successfully"}), 200

# Route for updating location data
@app.route("/projects/<project_id>/locations/<location_id>", methods=["PUT"])
def update_location(project_id, location_id):
    data = request.json
    locations_collection.update_one(
        {"_id": ObjectId(location_id)},
        {"$set": data}
    )
    return jsonify({"message": "Location updated successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)