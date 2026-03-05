## Social Media App

This project is a backend API that allows users to register, log in, create posts, and add comments. Once logged in, you can create, update, and delete your own posts and comments.

If you are registered as an admin, you can update or delete comments made by other users.

The app also includes an AI chatbot feature that lets you ask questions, powered by Ollama and the Mistral model. This feature is optional and requires downloading a ~4GB model.

Additionally, the app can send welcome emails to users when they register. To enable this, configure your email in the .env file.

### Features

User authentication (OAuth2 + JWT)

Post creation, updating, and deletion

Comment creation, updating, and deletion

Track user activities

AI chatbot (optional)

Email notifications (optional)

### Tech Stack

#### Backend & Frameworks:

FastAPI – modern, fast Python web framework

Pydantic – data validation and settings management

SQLAlchemy – ORM for database modeling and queries

Alembic – database schema migrations

#### Authentication & Security:

OAuth2 – user authentication

JWT (JSON Web Tokens) – token-based authentication

#### Database & Storage:

PostgreSQL – relational database

Docker volumes – persist database data

#### AI Integration (Optional):

Ollama – local AI model runner

Mistral model – language model for chatbot

#### Containerization & Dev Tools:

Docker & Docker Compose – containerization and orchestration

Git – version control

#### Utilities:

Email sending via SMTP configured in .env

Async programming for concurrent API requests

### Requirements

Git

Docker Desktop

### Installation

#### Create a folder for the project

mkdir foldername
cd foldername

#### Clone the repository

git clone https://github.com/Menarddddd/social-media-app
cd social-media-app

#### Start Docker containers

docker-compose up --build

#### Optional: Pull the Mistral AI model

To use the AI chatbot (~4GB download):

docker exec -it ollama ollama pull mistral

#### Access the API documentation

Open your browser and go to:
http://127.0.0.1:8000/docs

### Notes

The AI feature is optional. You can still use all other features without downloading the Mistral model.

Email notifications require setting up your SMTP configuration in the .env file.

### Quick Start

Register a user

Log in to receive an access token

Create posts and comments

Interact with the AI chatbot (if Mistral is installed)
