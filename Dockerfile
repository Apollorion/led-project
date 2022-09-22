FROM ubuntu:20.04

ENV CONSUMER_KEY=""
ENV CONSUMER_SECRET=""
ENV ACCESS_TOKEN=""
ENV ACCESS_SECRET=""
ENV BAD_WORDS_API_KEY=""

RUN apt-get update && apt-get install -y git make build-essential python3 python3-pip python3-distutils python3-dev \
    && $(which python3) -m pip install Pillow \
    && git clone https://github.com/hzeller/rpi-rgb-led-matrix.git \
    && cd rpi-rgb-led-matrix \
    && make build-python PYTHON=$(which python3) \
    && make install-python PYTHON=$(which python3) \
    && mkdir /app

RUN $(which python3) -m pip install tweepy requests

COPY . /app

ENTRYPOINT ["python3", "-u", "/app/run_text.py"]