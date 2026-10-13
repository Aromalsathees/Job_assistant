web: gunicorn --chdir backend core.wsgi:application --bind 0.0.0.0:$PORT --workers 3
worker: python backend/manage.py run_discovery
