web: gunicorn hc.wsgi --log-file -b 0.0.0.0:$PORT -w 2
migrate: ./manage.py migrate
triggers: ./manage.py ensuretriggers
