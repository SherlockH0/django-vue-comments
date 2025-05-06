#!/usr/bin/env sh

poetry run celery -A backend.project worker -l INFO
