# BookHaven Django

BookHaven Django is a server-rendered Django application for browsing books, categories, favorites, authentication, checkout, and payment screens. The project is now structured for a professional DevOps workflow with Docker, PostgreSQL, environment-based settings, and GitHub Actions CI.

## Stack

- Python 3.12
- Django
- PostgreSQL for Docker/production
- SQLite fallback for quick local development
- Gunicorn
- WhiteNoise for static files
- Docker and Docker Compose
- GitHub Actions CI

## Project Structure

```text
bookhaven_django/
├── bookhaven_django/          # Django project settings, ASGI, WSGI, root URLs
├── library/                   # Django app: models, forms, views, URLs, admin, migrations
├── templates/                 # Django templates
├── static/                    # Source static assets
├── media/                     # Uploaded and seeded book cover images
├── scripts/entrypoint.sh      # Container startup: wait DB, migrate, collectstatic, run command
├── .github/workflows/ci.yml   # GitHub Actions pipeline
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── requirements.txt
└── manage.py
```

## Environment Variables

Copy the example file before running Docker:

```bash
cp .env.example .env
```

Important variables:

- `DJANGO_SECRET_KEY`: production secret key
- `DJANGO_DEBUG`: `True` or `False`
- `DJANGO_ALLOWED_HOSTS`: comma-separated allowed hosts
- `DJANGO_CSRF_TRUSTED_ORIGINS`: comma-separated trusted origins
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`: PostgreSQL credentials
- `DJANGO_PORT`: host port exposed by Docker Compose

## Run With Docker

```bash
docker compose up --build
```

Then open:

```text
http://127.0.0.1:8000/
```

Useful Docker commands:

```bash
docker compose down
docker compose down -v
docker compose logs -f web
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py shell
```

## Run Locally Without Docker

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

By default, if PostgreSQL variables are not set, Django uses local SQLite.

## Static And Media Files

- Source static files are in `static/`
- Collected static files go to `staticfiles/`
- Uploaded/media files are stored in `media/`
- Docker Compose stores static and media data in named volumes

## CI/CD

The GitHub Actions pipeline in `.github/workflows/ci.yml` runs on every push and pull request targeting `main`.

Pipeline steps:

- install Python 3.12
- install dependencies
- run `python manage.py check`
- run migrations
- run Django tests
- run `collectstatic`
- build the Docker image
- validate and build Docker Compose services

## Git Commands

```bash
git init
git add .
git commit -m "Prepare Django project for Docker and CI"
git branch -M main
git remote add origin https://github.com/<your-user>/<your-repo>.git
git push -u origin main
```

## Production Notes

- Set `DJANGO_DEBUG=False`
- Use a strong `DJANGO_SECRET_KEY`
- Set real `DJANGO_ALLOWED_HOSTS`
- Set `DJANGO_CSRF_TRUSTED_ORIGINS` for HTTPS domains
- Use managed PostgreSQL or a secured database service
- Serve media files through object storage or a reverse proxy in production
