FROM thinkwhere/gdal-python:3.7-ubuntu as base

ENV PYTHONUNBUFFERED=1

ENV FLASK_DIR=/api_flask

WORKDIR $FLASK_DIR

RUN apt-get -y install python3

RUN apt-get -y install python3-pip

RUN pip3 install --upgrade pip

FROM base as with-requirements

COPY requirements.txt $FLASK_DIR/

RUN pip3 install -r requirements.txt