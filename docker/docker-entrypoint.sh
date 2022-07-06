#!/usr/bin/env bash
if [ ! -f /app/app.py ]; then
    echo "Flask app not found, dumping to shell"
    exec bash
fi
FLASK_APP=/app/app.py FLASK_ENV=development flask run --host=0.0.0.0
