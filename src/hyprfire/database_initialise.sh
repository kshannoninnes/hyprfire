#!/usr/bin/env bash

psql postgres -c "CREATE DATABASE hyprfiredb"
python manage.py makemigrations
python manage.py migrate

