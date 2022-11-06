#!/usr/bin/env bash

set -e
echo "Starting Videoshare"

# TODO: Migrate database
echo "Running database migrations"

# Run application
# exec is used here so the script will transfer the PID 1 to the app server when used in a docker container
# This enables signal capture within the application for easier graceful shutdown implementation
exec gunicorn -c gunicorn.py "videoshare.wsgi:application"
