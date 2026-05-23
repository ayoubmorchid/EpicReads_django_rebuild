# EpicReads Django

[![CI](https://github.com/ayoubmorchid/EpicReads_django_rebuild/actions/workflows/ci.yml/badge.svg)](https://github.com/ayoubmorchid/EpicReads_django_rebuild/actions/workflows/ci.yml)

EpicReads is a server-rendered Django library application for browsing books,
categories, favorites, authentication, checkout, and payment screens. The project
is prepared for a DevOps workflow with Git branches, Docker, PostgreSQL,
automated tests, and GitHub Actions CI/CD.

## Stack

- Python 3.12
- Django
- PostgreSQL with Docker Compose
- SQLite fallback for local development without Docker
- Gunicorn
- WhiteNoise
- Docker and Docker Compose
- GitHub Actions
- GitHub Container Registry

## Project Structure

```text
bookhaven_django/
├── bookhaven_django/          # Django settings, ASGI, WSGI, root URLs
├── library/                   # App: models, forms, views, URLs, admin, migrations
├── templates/                 # Django templates
├── static/                    # CSS, JavaScript, and source assets
├── media/                     # Uploaded and seeded book covers
├── scripts/entrypoint.sh      # Container startup script
├── .github/workflows/ci.yml   # GitHub Actions pipeline
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── requirements.txt
└── manage.py
```

## Run With Docker

```bash
docker compose up --build
```

Open:

```text
http://localhost:8000/
```

Useful commands:

```bash
docker compose down
docker compose logs -f web
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py shell
```

## Environment Variables

Copy the example file before running Docker if you want custom values:

```bash
cp .env.example .env
```

Important variables:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `DJANGO_SERVE_MEDIA`
- `DJANGO_PORT`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`

## Run Without Docker

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

When PostgreSQL variables are not set, Django uses local SQLite.

## Tests

```bash
python manage.py check
python manage.py test
python manage.py collectstatic --noinput
```

## CI/CD

The GitHub Actions workflow runs on:

- every push to `main`
- every pull request targeting `main`

Pipeline steps:

- install Python dependencies
- run Django system checks
- apply migrations
- run automated tests
- collect static files
- build the Docker image
- validate and build Docker Compose services
- publish the Docker image to GitHub Container Registry on successful `main` pushes

Published image:

```text
ghcr.io/ayoubmorchid/epicreads-django:latest
```

## Git Workflow

The project uses:

- `main` for production-ready code
- `dev` for integration
- `feature/*` branches for focused work
- merge commits to preserve branch history

Commit messages follow a clear conventional style such as `feat:`, `fix:`,
`style:`, `chore:`, and `merge:`.

## Production Notes

- Set `DJANGO_DEBUG=False`
- Use a strong `DJANGO_SECRET_KEY`
- Configure real `DJANGO_ALLOWED_HOSTS`
- Configure `DJANGO_CSRF_TRUSTED_ORIGINS` for HTTPS domains
- Use managed PostgreSQL or a secured database service
- Serve media files through object storage or a reverse proxy in production
