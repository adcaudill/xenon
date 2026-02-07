#!/bin/sh
set -x
ls -l /app
ls -l /app/xenon
echo "Starting Gunicorn..."
exec pipenv run gunicorn -b 0.0.0.0:5000 --log-level debug xenon.app:app
