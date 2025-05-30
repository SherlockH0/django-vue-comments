FROM python:3.13.3

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH .

ENV POETRY_NO_INTERACTION=1 
ENV POETRY_VIRTUALENVS_IN_PROJECT=1 
ENV POETRY_VIRTUALENVS_CREATE=1 
ENV POETRY_CACHE_DIR=/tmp/poetry_cache


RUN apt-get update \
    && apt-get install tidy>=5.6.0 --no-install-recommends -y \
    && pip install --no-cache-dir poetry==2.1.2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY poetry.lock pyproject.toml ./
COPY README.md Makefile ./

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

COPY backend backend
COPY scripts scripts

RUN chmod a+x scripts/*

ENTRYPOINT [ "./scripts/entrypoint.sh" ]
