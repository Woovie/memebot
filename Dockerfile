FROM python:latest
COPY . /basedir
WORKDIR /basedir

RUN pip install -r requirements.txt

RUN ["python", "main.py"]