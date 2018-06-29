web: gunicorn --log-file - -b 0.0.0.0:$PORT -w 2 hc.wsgi
migrate: ./manage.py migrate
triggers: ./manage.py ensuretriggers
