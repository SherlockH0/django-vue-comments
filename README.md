# django-vue-comments 💬

Comments SPR with Django on backend and Vue on frontend

##### Table of Contents

- [Demo](#demo)
- [Tech Stack](#tech-stack)
- [Usage](#usage)
  - [Run with docker](#run-with-docker)
  - [Development](#development-and-running-tests)
- [Features](#features)
- [API Docs](#api-docs)
  - [Authentication](#authentication)

<!-- ## Demo -->
<!---->
<!-- [![Watch the video]()](https://youtu.be/MnOoMGSmVR8) -->

## Tech Stack

### Backend

- [Django](https://www.djangoproject.com/)
- [Dajngo REST Framework](https://www.django-rest-framework.org/)
- [Celery](https://docs.celeryq.dev/en/stable/)
- [Django Channels](https://channels.readthedocs.io/en/latest/)
- [Redis](https://redis.io/)
- [PostgreSQL](https://www.postgresql.org/)
- [Poetry](https://python-poetry.org/)

### Frontend

- [Vite](https://vite.dev/)
- [Vue.js](https://vuejs.org/)
- [axios](https://axios-http.com/)
- [daisyUI](https://daisyui.com/)

### Hosting

- [Docker](https://www.docker.com/)
- [nginx](https://nginx.org/)

## Features

- Real-time comment updates via WebSockets.
- JWT-based authentication.
- Automatic resizing of large uploaded images.
- CAPTCHA protection to prevent spam.
- Dockerized setup for easy deployment.

## Usage

### Run with docker

Clone the repo, and `cd` into it:

```bash
git clone https://github.com/SherlockH0/django-vue-comments.git
cd django-vue-comments
```

Then, you can run the application using `docker compose`.

Create local settings files:

```bash
mkdir -p backend/local
cp backend/backend/project/settings/templates/settings.prod.py ./backend/local/settings.prod.py
cp frontend/env/.env.production.example frontend/.env.production
```

Run the application:

```bash
docker compose up
```

Application is now available on <http://localhost>

### Development

For development, see the [backend](backend/README.md) and [frontend](frontend/README.md) README's.

## API Docs

### Authentication

Application implements a simple JWT authentication.

To create a user, make a `POST` request to the `/api/auth/register/` route.

To log user in, obtain access and refresh tokens by making a `POST` request to the `api/token/` route.

To access protected routes, add a `Authorization` header into your request:

```
Authorization: Bearer <token>
```
