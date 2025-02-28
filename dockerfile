FROM python:3.12

COPY requirements.txt /temp/requirements.txt
COPY marketplace /marketplace
WORKDIR /marketplace
EXPOSE 8000

RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user

USER service-user
