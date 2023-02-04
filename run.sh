#!/bin/sh

set -a # auto-export all variables
source docker_compose.env
set +a

python3 manage.py makemigrations
python3 manage.py migrate

# gunicorn contractsecurityapp.wsgi --workers 3 --log-level debug
python3 manage.py runserver
