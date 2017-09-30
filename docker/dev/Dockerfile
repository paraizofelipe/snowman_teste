FROM python:alpine
MAINTAINER Felipe Paraizo <felipeparaizo@gmail.com>

EXPOSE 8000

COPY . /src

WORKDIR /src

ENV PYTHONPATH .

RUN pip3 install gunicorn
RUN pip3 install -r requirements.txt

VOLUME /src

CMD gunicorn --reload --bind=0.0.0.0:8000 snowman_teste.server:__hug_wsgi__