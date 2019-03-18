FROM tiangolo/uwsgi-nginx-flask:flask-python3.5-index-upload
# maybe we want to move to:
# FROM tiangolo/meinheld-gunicorn-flask:python3.6

MAINTAINER Akshay Dahiya <xadahiya@gmail.com>

COPY ./requirements.txt requirements.txt
RUN pip install -U pip && pip install --upgrade pip setuptools \ 
      && pip install -r requirements.txt && rm -rf *

COPY  . /app

ENV PYTHONPATH $PYTHONPATH:/app:/app/hydrus

RUN mv /app/hydrus/uwsgi.ini /app/uwsgi.ini

ENV MESSAGE "Hail Hydra"
