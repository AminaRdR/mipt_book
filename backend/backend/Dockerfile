# FROM python:3.11.1-alpine3.17
# FROM python:3.11.1-bullseye
# FROM python:3.11.1-buster
# FROM python:3.11.1-slim
FROM python:3.11.1-bullseye

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psycopg2-binary


ENV LIBRD_VER=1.3.0

RUN pip install Pyrebase4
RUN pip install confluent_kafka

RUN pip install kafka-python
RUN pip install gevent 
RUN pip install whitenoise

COPY . .

EXPOSE 8000
WORKDIR /usr/src/app

# 1) CMD ["django-admin", "startproject", "backend"]

# 2.1) CMD ["cd", ".."]
# 2.2) CMD ["python", "manage.py", "migrate"]
# 2.3) CMD ["python", "manage.py", "startapp", "main"]
# 2.4) CMD ["python", "manage.py", "startapp", "users"]

# 3.1) docker ps -a
# 3.2) docker exec -it container_id python manage.py createsuperuser

#CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
#CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runsslserver --certificate mipt.crt --key mipt.key 0.0.0.0:8000"]
CMD ["sh", "-c", "gunicorn -c gunicorn.conf.py --certfile=mipt.crt --keyfile=mipt.key backend.wsgi:application --log-level debug"]


# ANY OTHER COMMANDS:
#CMD ["python", "manage.py", "makemigrations"]
#CMD ["python", "manage.py", "migrate"]
#CMD ["python", "manage.py", "migrate", "sessions"]
#CMD ["exec", "gunicorn", "prod.wsgi:application", "-b", "0.0.0.0:8000", "--reload"]
#CMD ["python", "manage.py", "runsslserver", "--certificate", "rootCA.crt", "--key", "rootCA.key", "0.0.0.0:8000"]
#CMD ["python", "manage.py", "createsuperuser"]

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["sh", "-c", "echo 'y' | python manage.py makemigrations --merge && python manage.py runserver 0.0.0.0:8000"]
