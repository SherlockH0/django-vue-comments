FROM python:3.13.3

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH .

ENV BACKEND_SETTING_DATABASES '{"default":{"HOST":"db"}}'
ENV BACKEND_SETTING_LOCAL_SETTINGS_PATH "local/settings.dev.py"
ENV BACKEND_SETTING_CELERY_BROKER_URL "redis://broker:6379/1"
ENV BACKEND_SETTING_CACHES '{"default":{"LOCATION":"redis://broker:6379/2"}}'
ENV BACKEND_SETTING_ALLOWED_HOSTS '["localhost"]'
ENV BACKEND_SETTING_CHANNEL_LAYERS '{ "default": { "CONFIG": { "hosts": [{"address": "redis://broker:6379/3"}] }}}'

RUN set -xe \
    && pip install --no-cache-dir poetry==2.1.2 \
    && poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root

COPY README.md Makefile ./

COPY scripts scripts

RUN chmod a+x scripts/*

ENTRYPOINT [ "./scripts/entrypoint.sh" ]
