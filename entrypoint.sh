#!/bin/sh
cd price_tracker
python manage.py migrate --no-input

exec "$@"
