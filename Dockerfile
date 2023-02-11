# FROM ubuntu:latest
FROM python:3.9.16

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /requirements.txt

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip3 install -r requirements.txt

WORKDIR /app
COPY . /app/

ENV PORT=8000
EXPOSE 8000
EXPOSE 3500
EXPOSE 80
