release: python manage.py collectstatic --noinput
web: gunicorn ecommerce.wsgi:application --log-file -
