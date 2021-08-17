# FROM python:3.8
# WORKDIR /fastapi-app
# COPY requirements.txt .
# RUN pip install -r requirements.txt
# COPY ./app ./app
# COPY gunicorn_config.py gunicorn_config.py
# CMD ["python","./app/main.py"]

from python:3.8.6-buster
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
COPY main.py main.py
COPY gunicorn_config.py gunicorn_config.py
RUN pip install -r requirements.txt
EXPOSE 8000
CMD  gunicorn -c gunicorn_config.py --bind=0.0.0.0 -p 8000 main:app