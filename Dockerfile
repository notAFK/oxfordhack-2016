FROM eboraas/apache-php

MAINTAINER thee-engineer <copil.alexander@gmail.com>

RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y python && \
    apt-get install -y python-pip && \
    apt-get install -y gcc && \
    apt-get install -y cpython && \
    mkdir /proj

COPY . /proj/
COPY ceva.html /var/www/html/index.html

RUN pip install --upgrade pip && \
    pip install -r /proj/requierments.txt
