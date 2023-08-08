FROM python:3.9

WORKDIR /app

COPY requirements/requirements.txt /app

RUN apt-get update && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app
