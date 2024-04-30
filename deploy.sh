#!/bin/bash

# Pull the latest images from Docker Hub (if necessary)
docker-compose -f docker-compose.yml pull

# Stop and remove existing containers
docker-compose -f docker-compose.yml down

# Start the containers in detached mode
docker-compose -f docker-compose.yml up -d
