# Social Media App (FastAPI)

A simple social media backend + server-rendered web UI built with **FastAPI**, **SQLAlchemy (Async)**, **PostgreSQL**, and **Jinja2 + Bootstrap**.

## Features

- User authentication (JWT access token in HttpOnly cookie for web)
- Sign up / Sign in / Logout
- Profile page
  - Update profile details
  - Upload profile picture
- Feed
  - Create post
  - Comment on posts
  - Pagination
- View other users’ profiles
- Soft delete users (optional depending on your implementation)

## Tech Stack

- FastAPI
- SQLAlchemy Async
- PostgreSQL
- Alembic (migrations)
- Jinja2 Templates + Bootstrap
- Docker + Docker Compose

---

## Project Structure (high-level)

- `app/routers/api/` - JSON API routes
- `app/routers/web/` - Web (Jinja) routes
- `app/services/` - business logic
- `app/repositories/` - database access
- `app/templates/` - HTML templates
- `app/static/` - icons/static assets
- `app/media/` - uploaded profile pictures (local dev)

---

## Running with Docker Compose

- Create .env file first, follow the .env.example
- In terminal run docker-compose up --build
