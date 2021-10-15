#!/usr/bin/env python
# Display a runtext with double-buffering.
import time
import sys
import os
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from rgbmatrix import graphics
import tweepy
import os
import random

DEFAULT_TEXT = "This is my LED Sign, I love it."

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
    my_text = DEFAULT_TEXT
    while True:

        print("Retreiving Mentions")
        last_id = get_last_tweet()
        req = {}
        if last_id != 0:
            req = {
                "since_id": last_id,
                "tweet_mode": "extended"
            }
        mentions = api.mentions_timeline(**req)

        if len(mentions) > 0:
            for mention in reversed(mentions):
                print("Starting new mention")

                # note and store last tweet
                new_id = mention.id
                put_last_tweet(new_id)

                # Print the Tweet onto the sign
                my_text = mention.text.replace("@Apollorion ", "", 1)
                display_text(my_text)
                print("Ending Mention")
        else:
            #Display either the last tweet or the default text
            display_text(my_text)


def display_text(my_text, seconds=60):
    offscreen_canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("fonts/7x13B.bdf")
    textColor = graphics.Color(random.randint(0,255), random.randint(0,255), random.randint(0,255))
    pos = offscreen_canvas.width


    run_seconds = 0
    while run_seconds < seconds:
        offscreen_canvas.Clear()
        length = graphics.DrawText(offscreen_canvas, font, pos, 12, textColor, my_text)
        pos -= 1
        if (pos + length < 0):
            pos = offscreen_canvas.width

        time.sleep(0.05)
        run_seconds += 0.05
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

def get_last_tweet():
    f = open("tweet_ID.txt", 'r')
    lastId = int(f.read().strip())
    f.close()
    return lastId

def put_last_tweet(Id):
    f = open("tweet_ID.txt", 'w')
    f.write(str(Id))
    f.close()
    return

try:
    print("Press CTRL-C to stop")
    run()
except KeyboardInterrupt:
    print("Exiting\n")
    sys.exit(0)