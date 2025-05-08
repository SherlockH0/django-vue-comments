# Installation instructions

Make sure you have necessary dependencies installed:

- [Docker](https://www.docker.com/)
- [Python ^3.13](https://www.python.org/)
- [tidy](https://www.html-tidy.org/)
- [Poetry](https://python-poetry.org/)
- `file` (see [python-magic](https://pypi.org/project/python-magic/) installation instructions)

Start `PostgreSQL` and `Redis` with `docker`:

```bash
make deps
```

In a different terminal, create local settings files:

```bash
mkdir -p local
cp backend/project/settings/templates/settings.dev.py ./local/settings.dev.py
```

Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install the project using `poetry`, migrate the database:

```bash
make update
```

Create superuser (optional):

```bash
make superuser
```

Run local server:

```bash
make runserver
```

In a different terminal start `celery` worker:

```bash
make celery
```

To make migrations after changes in the models, run:

```bash
make migrations
```

To migrate, run:

```bash
make migrate
```
