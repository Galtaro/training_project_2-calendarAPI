#!/bin/sh

python manage.py migrate --no-input
python manage.py create_country
python manage.py create_official_holidays

gunicorn --bind 0.0.0.0:8000 --workers=4 calendarAPI.wsgi:application