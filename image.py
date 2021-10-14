#!/usr/bin/env python
import time
import sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

# Configuration for the matrix
options = RGBMatrixOptions()
options.hardware_mapping = "adafruit-hat"
options.rows = 16
options.cols = 32
options.chain_length = 3
options.parallel = 1
options.row_address_type = 0
options.multiplexing = 4
options.pwm_bits = 11
options.brightness = 10
options.pwm_lsb_nanoseconds = 130
options.led_rgb_sequence = "RGB"
options.pixel_mapper_config = ""
options.panel_type = ""
options.drop_privileges=False


def run(image_file):
    image = Image.open(image_file)
    matrix = RGBMatrix(options = options)
    image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
    matrix.SetImage(image.convert('RGB'))

try:
    print("Press CTRL-C to stop.")
    run(sys.argv[1])
    while True:
        time.sleep(1000)
except KeyboardInterrupt:
    sys.exit(0)