FROM tiangolo/uwsgi-nginx-flask:flask-python3.5-index-upload

MAINTAINER Akshay Dahiya <xadahiya@gmail.com>


COPY ./requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt

RUN rm -rf *

COPY  ./hydrus/ /app/hydrus/

ENV PYTHONPATH $PYTHONPATH:/app/

RUN mv hydrus/uwsgi.ini ./uwsgi.ini

ENV MESSAGE "Hail Hydra"
