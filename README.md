# EpicReads / BookHaven Django

A server-rendered Django bookstore-style application for browsing books, categories, favorites, authentication, checkout, and payment screens.

This project is presented as a junior full-stack and DevOps learning project. It shows how a Django application can be structured with environment-based settings, Docker, PostgreSQL, static file handling, tests, and GitHub Actions CI.

## Features

- Public book browsing pages
- Book categories and detail pages
- User authentication screens
- Favorites, cart, checkout, and payment flow screens
- Admin-managed book and media content
- Static and media file handling
- Docker setup with PostgreSQL
- GitHub Actions workflow for checks, tests, static collection, and Docker build verification

## Tech Stack

- Python 3.12
- Django 5
- PostgreSQL for Docker/production-like setup
- SQLite fallback for quick local development
- Gunicorn
- WhiteNoise
- Docker and Docker Compose
- GitHub Actions CI

## Project Structure

```text
bookhaven_django/
|-- bookhaven_django/          # Django project settings, ASGI, WSGI, root URLs
|-- library/                   # Django app: models, forms, views, URLs, admin, migrations
|-- templates/                 # Django templates
|-- static/                    # Source static assets
|-- media/                     # Uploaded and seeded book cover images
|-- scripts/entrypoint.sh      # Container startup helper
|-- .github/workflows/ci.yml   # GitHub Actions pipeline
|-- Dockerfile
|-- docker-compose.yml
|-- .dockerignore
|-- .env.example
|-- requirements.txt
`-- manage.py
```

## Local Setup Without Docker

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

By default, if PostgreSQL variables are not set, Django uses local SQLite.

## Run With Docker

Copy the example environment file first:

```bash
cp .env.example .env
```

Start the application:

```bash
docker compose up --build
```

Open:

```text
http://127.0.0.1:8000/
```

Useful Docker commands:

```bash
docker compose down
docker compose down -v
docker compose logs -f web
docker compose exec web python manage.py createsuperuser
```

## Environment Variables

Important variables:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `DJANGO_PORT`

## CI And DevOps Notes

The GitHub Actions workflow runs on pushes and pull requests targeting `main`.

The pipeline checks:

- Python dependency installation
- `python manage.py check`
- database migrations
- Django tests
- static file collection
- Docker image build
- Docker Compose configuration and build

## What I Practiced

- Organizing a Django project for clearer local and Docker-based development
- Using environment variables instead of hard-coded production settings
- Connecting Django with PostgreSQL in Docker Compose
- Adding a CI workflow for automated checks and build validation
- Improving Git workflow with feature branches and pull requests

## Status

Portfolio learning project. The application is suitable for demonstrating Django fundamentals, Docker setup, CI basics, and project documentation.