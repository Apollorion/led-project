#!/usr/bin/env python
# Display a runtext with double-buffering.
import os
import time
import sys
import requests
import random
from tracks import tracks

announcement = "88.5 FM - Vote for the next song at christmas-on-kohler.com!"

def run():
    API_ENDPOINT="http://fpp.lan/api/fppd/status"
    while True:
        status = requests.get(API_ENDPOINT).json()
        current_song = status["current_song"]
        if current_song in dict.keys(tracks):
            this = tracks[current_song]
            display_text(f"88.5 FM - Now Playing: {this['Title']} by {this['Artist']}", seconds=10)
            display_text(announcement, seconds=15)
        else:
            display_text(announcement, seconds=10)



def display_text(my_text, seconds=60):
    if "LOCAL" not in os.environ:
        from matrix import display_text as dt
        dt(my_text, seconds=seconds)
    else:
        print(my_text)
        time.sleep(seconds)

try:
    print("Press CTRL-C to stop")
    run()
except KeyboardInterrupt:
    print("Exiting\n")
    sys.exit(0)