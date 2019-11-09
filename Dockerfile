FROM python:3.7-alpine

RUN pip install argparse mysql-connector-python beautifulsoup4 requests

COPY . /usr/src/themoviepredictor

WORKDIR /usr/src/themoviepredictor

# CMD python /usr/src/themoviepredictor/app.py CMD au démarrage