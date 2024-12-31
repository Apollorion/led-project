#!/usr/bin/env python
# Display a runtext with double-buffering.
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from rgbmatrix import graphics
import random
import pathlib

current_dir = str(pathlib.Path(__file__).parent.resolve())

# LED Sign options
options = RGBMatrixOptions()
options.hardware_mapping = "adafruit-hat"
options.rows = 16
options.cols = 32
options.chain_length = 3
options.parallel = 1
options.row_address_type = 0
options.multiplexing = 4
options.pwm_bits = 11
options.brightness = 30
options.pwm_lsb_nanoseconds = 130
options.led_rgb_sequence = "RGB"
options.pixel_mapper_config = ""
options.panel_type = ""
options.drop_privileges=False

matrix = RGBMatrix(options = options)

def display_text(my_text_arr, timeout=30):
    offscreen_canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont(current_dir + "/fonts/7x13B.bdf")
    textColor = graphics.Color(random.randint(0,255), random.randint(0,255), random.randint(0,255))

    for line in my_text_arr:
        offscreen_canvas.Clear()

        graphics.DrawText(offscreen_canvas, font, 0, 12, textColor, '{:^12}'.format(line))
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

        time.sleep(timeout)

    return my_text_arr

def scroll_text(my_text, seconds=60):

    offscreen_canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont(current_dir + "/fonts/7x13B.bdf")
    textColor = graphics.Color(random.randint(0,255), random.randint(0,255), random.randint(0,255))
    pos = offscreen_canvas.width

    run_seconds = 0
    is_off_screen = False
    while not is_off_screen:
        offscreen_canvas.Clear()
        length = graphics.DrawText(offscreen_canvas, font, pos, 12, textColor, my_text)
        pos -= 1
        if (pos + length < 0):
            pos = offscreen_canvas.width

            if run_seconds > seconds:
                is_off_screen = True

        time.sleep(0.05)
        run_seconds += 0.05
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

    return my_text
