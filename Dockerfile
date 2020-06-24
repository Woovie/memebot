FROM python:latest
WORKDIR /basedir
COPY . /basedir

RUN ["python", "main.py"]