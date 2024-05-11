FROM python:3.12.2-alpine

WORKDIR /app

COPY ./backend/ /app/
COPY requirements.txt /app/
ADD .env.docker /app/.env

RUN apk update && apk add --no-cache curl \
    && pip install -r requirements.txt

CMD python manage.py migrate \
    && python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='root').exists() or User.objects.create_superuser(email='root@gmail.com', password='root', username='root')" \
#    && python manage.py seed_all \
    && python manage.py collectstatic --no-input \
    && gunicorn podiya.wsgi:application --bind 0.0.0.0:8000 --log-level info
ls