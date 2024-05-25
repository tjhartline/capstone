web: python -m pip install --upgrade pip
web: pip install -r requirements.txt
web: gunicorn wsgi:server --workers 2 --threads 4 --timeout 0
