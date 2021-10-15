#!/usr/bin/env python
# Display a runtext with double-buffering.
import time
import sys
import os
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from rgbmatrix import graphics
import tweepy
import os

# Authenticate to Twitter
auth = tweepy.OAuthHandler(os.environ["CONSUMER_KEY"], os.environ["CONSUMER_SECRET"])
auth.set_access_token(os.environ["ACCESS_TOKEN"], os.environ["ACCESS_SECRET"])
api = tweepy.API(auth)

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
options.brightness = 10
options.pwm_lsb_nanoseconds = 130
options.led_rgb_sequence = "RGB"
options.pixel_mapper_config = ""
options.panel_type = ""
options.drop_privileges=False

matrix = RGBMatrix(options = options)

def run():
    offscreen_canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("fonts/7x13B.bdf")
    textColor = graphics.Color(255, 0, 0)
    pos = offscreen_canvas.width


    while True:
        print("Retreiving Mentions")
        mentions = api.mentions_timeline()
        if len(mentions) == 0:
            return

        for mention in reversed(mentions):
            print("Starting new mention")

            new_id = mention.id
            my_text = mention.text.replace("@Apollorion ", "", 1)

            # Print the Tweet onto the sign
            run_seconds = 0
            while run_seconds < 10:
                print("Displaying mention for 10 seconds")
                offscreen_canvas.Clear()
                length = graphics.DrawText(offscreen_canvas, font, pos, 12, textColor, my_text)
                pos -= 1
                if (pos + length < 0):
                    pos = offscreen_canvas.width

                time.sleep(0.05)
                run_seconds += 0.05
                offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
            print("Ending Mention")

try:
    print("Press CTRL-C to stop")
    run()
except KeyboardInterrupt:
    print("Exiting\n")
    sys.exit(0)