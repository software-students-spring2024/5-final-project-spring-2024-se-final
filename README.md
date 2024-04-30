# Final Project

An exercise to put to practice software development teamwork, subsystem communication, containers, deployment, and CI/CD pipelines. See [instructions](./instructions.md) for details.

[![Web App CI/CD](https://github.com/software-students-spring2024/5-final-project-spring-2024-se-final/actions/workflows/webapp-workflow.yml/badge.svg?branch=main)](https://github.com/software-students-spring2024/5-final-project-spring-2024-se-final/actions/workflows/webapp-workflow.yml)

[![MongoDB CI/CD](https://github.com/software-students-spring2024/5-final-project-spring-2024-se-final/actions/workflows/mongodb-workflow.yml/badge.svg?branch=main)](https://github.com/software-students-spring2024/5-final-project-spring-2024-se-final/actions/workflows/mongodb-workflow.yml)

[Container Images on Docker Hub](https://hub.docker.com/r/zhongqianchen/wbm/tags)

## Description

This project is a world build manager web application working with the following functions:
1. User can create new project for their world building in the app with a title and description.
2. User can add new characters & locations with customized details to a specific project.
3. User can edit any details they want by accessing the project / character / location details page and save the changes.
4. User can delete any project / character / location they would like to discard.

## Team members

[Zhongqian Chen (John)](https://github.com/ZhongqianChen) (https://github.com/ZhongqianChen)

[Eric Emmendorfer](https://github.com/ericemmendorfer) (https://github.com/ericemmendorfer)

[Hojong Shim](https://github.com/HojongShim) (https://github.com/HojongShim)

[Ethan Kim](https://github.com/ethanki) (https://github.com/ethanki)

## Instructions

You could directly access and use the public web page deployed on Digital Ocean right [here](http://142.93.12.105:5000).

Alternatively, you could run this web app on your local machine by following these steps:
1. Fully intall Docker and Docker Desktop on your local machine.
2. Open the directory's root folder and run the command `docker-compose up --build`.
3. Access your [localhost page](http://localhost:5000) and the web app should be running there.
4. If you want to stop the program from running, simply press `Ctrl+C` at the terminal you were running `docker-compose up --build` from.

There is no need for any starter data for this web app to run, so follow the above steps correctly and you should be able to use the web app as intended.