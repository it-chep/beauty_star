#!/bin/bash
DJANGO_SETTINGS_MODULE=beauty_star.settings python -m celery -A main_site.celery worker -B -E --loglevel INFO --concurrency=4 &
python manage.py runserver 0:8000