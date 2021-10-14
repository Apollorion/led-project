#!/usr/bin/env python
# Display a runtext with double-buffering.
import time
import sys
import os
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from rgbmatrix import graphics

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

matrix = RGBMatrix(options = options)

def run(text):
    offscreen_canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("fonts/7x13B.bdf")
    textColor = graphics.Color(255, 0, 0)
    pos = offscreen_canvas.width
    my_text = text

    while True:
        offscreen_canvas.Clear()
        len = graphics.DrawText(offscreen_canvas, font, pos, 12, textColor, my_text)
        pos -= 1
        if (pos + len < 0):
            pos = offscreen_canvas.width

        time.sleep(0.05)
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

try:
    # Start loop
    print("Press CTRL-C to stop sample")
    run("hello, world")
except KeyboardInterrupt:
    print("Exiting\n")
    sys.exit(0)