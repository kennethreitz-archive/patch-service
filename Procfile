web: gunicorn patchmaster:app -b 0.0.0.0:$PORT -k gevent -w 4
celeryd: ./manage.py celeryd --events --loglevel info