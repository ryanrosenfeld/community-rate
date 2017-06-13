release: python dev/manage.py makemigrations && python dev/manage.py migrate
web: bash -c 'cd dev && gunicorn community_rate.wsgi --log-file -'