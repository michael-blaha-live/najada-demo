#!/bin/sh

echo "Running Database Migrations"
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata initial_data.json

echo "Running eshopapp1 management commands"
python manage.py "sample_management_command"

exec "$@"