# Social Media App

## This project allows you to create user and login. Once logged in you can create your own post(s) and make comment(s).

## You can also update and delete your comments and others if you are registered as an admin role

## There's also an AI that you can ask question

## This app allows you to send an email, if you want you can put an email in .env. Once you set that up and a user register with their real email, it will send a welcome email to them.

## Note

### The AI route requires you to download Mistral model(~4gb)

### This is optional you can still use the app without this AI

## Features

- User authentication
- Post creation and deletion
- Comment creation and deletion
- Track activities
- Bot you can ask (optional)

## Framework and tools

- Oauth2 for authentication
- JWT for web token
- FastAPI framework
- Postgres database
- AI ollama/mistral

# Requirements

- Git
- Docker Desktop

## Installation

### Create an empty folder

- mkdir foldername

### Go to the folder

- cd foldername

### Clone the repo

- git clone https://github.com/Menarddddd/social-media-app

### Run and create the containers

- docker-compose up --build

### Pull the Mistral model (OPTIONAL, IF YOU WANT THE AI)

- docker exec -it ollama ollama pull mistral

### It's all set up now you can go ahead and create an account and login

- open your browser and go to this http://127.0.0.1:8000/docs
