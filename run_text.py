#!/usr/bin/env python
# Display a runtext with double-buffering.
import os
import time
import sys
import requests
import random
import json
from datetime import date, timedelta

def run():

    while True:
        ice = get_sea_ice_cover()
        snow = get_snow_cover()

        display_text(ice, seconds=10)
        display_text(snow, seconds=10)


def get_sea_ice_cover():
    last_month = date.today().replace(day=1) - timedelta(days=1)
    m = last_month.strftime("%m")
    y = last_month.strftime("%Y")

    r = requests.get(f"https://www.ncei.noaa.gov/access/monitoring/snow-and-ice-extent/sea-ice/G/{m}/data.json")
    j = r.json()
    data = j["data"][y]
    return [
    #   "XXXXXXXXXXXXX"
        " Sea Ice Cov ", 
        f" Typ {data['value']} ", 
        f" Anom {data['anom']} "
    ]

def get_snow_cover():
    last_month = date.today().replace(day=1) - timedelta(days=1)
    m = last_month.strftime("%m")
    y = last_month.strftime("%Y")

    r = requests.get(f"https://www.ncei.noaa.gov/access/monitoring/snow-and-ice-extent/snow-cover/namgnld/{m}/data.json")
    j = r.json()
    data = j["data"][y]

    return [
    #   "XXXXXXXXXXXXX"
        "   Snow Cov  ", 
        f" Typ {data['value']} ", 
        f" Anom {data['anom']} "
    ]


def display_text(my_text_arr, seconds=60):
    if "LOCAL" not in os.environ:
        from matrix import display_text as dt
        dt(my_text_arr, timeout=seconds)
    else:
        for i in my_text_arr:
            print(i)

try:
    print("Press CTRL-C to stop")
    run()
except KeyboardInterrupt:
    print("Exiting\n")
    sys.exit(0)