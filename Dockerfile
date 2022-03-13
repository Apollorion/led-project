FROM ubuntu:20.04

RUN apt-get update && apt-get install -y git make build-essential python3 python3-distutils python3-dev \
    && git clone https://github.com/hzeller/rpi-rgb-led-matrix.git \
    && cd rpi-rgb-led-matrix \
    && make build-python PYTHON=$(which python3) \
    && make install-python PYTHON=$(which python3)