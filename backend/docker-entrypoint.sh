#!/bin/sh

uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000

# exec gunicorn --bind 0.0.0.0:5000 --forwarded-allow-ips='*' wsgi:app