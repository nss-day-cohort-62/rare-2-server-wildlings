#!/bin/bash

rm -rf rareapi/migrations
rm db.sqlite3
python manage.py migrate
python manage.py makemigrations rareapi
python manage.py migrate rareapi
python3 manage.py loaddata users tokens authors categories tags posts comments 
