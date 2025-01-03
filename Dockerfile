FROM ubuntu:20.04

RUN apt-get update && apt-get install -y git make build-essential python3 python3-pip python3-distutils python3-dev \
    && $(which python3) -m pip install Pillow \
    && git clone https://github.com/hzeller/rpi-rgb-led-matrix.git \
    && cd rpi-rgb-led-matrix \
    && git reset --hard 14ab2ff91453cc7d19a9a41ae1b415199abaf5a9 \
    && make build-python PYTHON=$(which python3) \
    && make install-python PYTHON=$(which python3) \
    && mkdir /app

RUN $(which python3) -m pip install requests

COPY . /app

ENTRYPOINT ["python3", "-u", "/app/run_text.py"]