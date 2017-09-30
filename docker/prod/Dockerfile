FROM python:alpine
MAINTAINER Felipe Paraizo <felipeparaizo@gmail.com>

EXPOSE 8000

COPY . /src

WORKDIR /src

ENV PYTHONPATH .

RUN pip3 install gunicorn
RUN pip3 install -r requirements.txt \
    && python snowman_teste/create_base.py

CMD python3 snowman_teste/run.py