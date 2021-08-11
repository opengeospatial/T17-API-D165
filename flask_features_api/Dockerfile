FROM tiangolo/uwsgi-nginx-flask:python3.6 as base

RUN mkdir -p /usr/src/app

COPY requirements.txt /usr/src/app/requirements.txt

RUN apt-get update && apt-get install -y --reinstall ca-certificates
RUN export REQUESTS_CA_BUNDLE=/etc/ssl/certs
RUN pip3 install --no-cache-dir -r /usr/src/app/requirements.txt

WORKDIR /usr/src/app
COPY . /usr/src/app

ENV UWSGI_INI /usr/src/app/uwsgi.ini
ENV LISTEN_PORT 8080

EXPOSE 8080

FROM base as prod
# use as it is, entrypoint configured in base image

FROM base as debug
# Debug image reusing the base
# Install dev dependencies for debugging
RUN pip install debugpy
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1



