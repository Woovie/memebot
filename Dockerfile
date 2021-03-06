FROM python:latest
COPY . /basedir
WORKDIR /basedir

RUN pip install -r requirements.txt

CMD ["python", "-u", "main.py"]