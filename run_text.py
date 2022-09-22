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
import pathlib
import requests

DEFAULT_TEXT = "See your tweet here, @Apollorion on twitter! Mess with my lights at joey.apollorion.com!"
TWEET_ID_FILE = "/tweets/tweet_ID.txt"
TRY_NASA_AFTER_X_CACHED_TWEETS = 2
DISPLAY_MY_TWEETS_FOR_X_SECONDS = 600
SKIP_PROFANITY_CHECK = ["NASA", "NASAHubble", "Space_Station", "NASAhistory", "esa", "NASAEarth", "BeamDental", "BarakObama", "StationCDRKelly", "SpaceX", "BernieSanders"]

current_dir = str(pathlib.Path(__file__).parent.resolve())

# Authenticate to Twitter
auth = tweepy.OAuthHandler(os.environ["CONSUMER_KEY"], os.environ["CONSUMER_SECRET"])
auth.set_access_token(os.environ["ACCESS_TOKEN"], os.environ["ACCESS_SECRET"])
api = tweepy.API(auth)

# Get who I follow
TWITTER_ACCOUNTS_TO_MONITOR = api.get_friend_ids(screen_name="apollorion")

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

def run():
    my_text = DEFAULT_TEXT
    none_count = 0
    unauthorized_count = 0
    while True:

        try:
            print("Retreiving Mentions")
            last_id = get_last_tweet()
            req = {}
            if last_id != 0:
                req = {
                    "since_id": last_id,
                    "tweet_mode": "extended",
                    "include_entities": False
                }
            mentions = api.mentions_timeline(**req)

            if len(mentions) > 0:
                none_count = 0
                for mention in reversed(mentions):
                    print("Starting new mention")

                    # note and store last tweet
                    new_id = mention.id
                    put_last_tweet(new_id)

                    screen_name = ""
                    if hasattr(mention, "user") and hasattr(mention.user, "screen_name"):
                        screen_name = mention.user.screen_name

                    # Print the Tweet onto the sign
                    my_text = process_tweet(mention, seconds=DISPLAY_MY_TWEETS_FOR_X_SECONDS, screen_name=f"@{screen_name}: ")
                    print("Ending Mention")
            else:
                #Display either the last tweet or the default text
                print("Nothing new, starting from cache")
                none_count += 1

                if none_count < TRY_NASA_AFTER_X_CACHED_TWEETS:
                    display_text(my_text, check_profanity=False)
                else:
                    none_count = 0
                    try_nasa()

            # reset to 0 if we get this far
            unauthorized_count = 0
        except tweepy.errors.Unauthorized:
            if unauthorized_count < 10:
                print("Unauthorized error. Trying again in 10 seconds.")
                time.sleep(10)
                unauthorized_count += 1
            else:
                print("too many unauthorizations, dying...")
                exit(1)

def try_nasa(max_tweets=2):
    print("trying nasa")

    user_id = TWITTER_ACCOUNTS_TO_MONITOR[random.randint(0, len(TWITTER_ACCOUNTS_TO_MONITOR) - 1)]
    user = api.get_user(user_id=user_id)
    tweets = api.user_timeline(user_id=user.id_str, count=max_tweets, include_rts=False, tweet_mode='extended', exclude_replies=True)
    for mention in reversed(tweets):
        profanity = False if user.screen_name in SKIP_PROFANITY_CHECK else True
        process_tweet(mention, check_profanity=profanity, screen_name=f"@{user.screen_name}: ")

def process_tweet(mention, check_profanity=True, seconds=60, screen_name=""):
    # Print the Tweet onto the sign
    # IDK Why but some tweets come in as "full_text" and some come in as "text" so we will just check for both
    if hasattr(mention, 'text'):
        my_text = screen_name + mention.text.replace("\n", "  ").replace("@Apollorion", "", 1).replace("@apollorion", "", 1)
        my_text = display_text(my_text, check_profanity=check_profanity, seconds=seconds)
    elif hasattr(mention, 'full_text'):
        my_text = screen_name + mention.full_text.replace("\n", "  ").replace("@Apollorion", "", 1).replace("@apollorion", "", 1)
        my_text = display_text(my_text, check_profanity=check_profanity, seconds=seconds)

    else:
        print("Mention has no text attribute")
        print(mention)
        my_text = DEFAULT_TEXT

    return my_text

def display_text(my_text, seconds=60, check_profanity=True):

    if check_profanity:
        print("Checking Profanity")
    else:
        print("Trusting Content")

    if check_profanity and contains_profanity(my_text):
        return DEFAULT_TEXT

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

def get_last_tweet():
    if os.path.exists(TWEET_ID_FILE):
        f = open(TWEET_ID_FILE, "r")
        lastId = int(f.read().strip())
        f.close()
        return lastId
    else:
        return 0

def put_last_tweet(Id):
    f = open(TWEET_ID_FILE, 'w')
    f.write(str(Id))
    f.close()
    return

def contains_profanity(text):
    url = "https://api.promptapi.com/bad_words"

    payload = text.encode("utf-8")
    headers= {
        "apikey": os.environ["BAD_WORDS_API_KEY"]
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        result = response.json()
        print("bad words result", result)
        if "bad_words_total" in result and result["bad_words_total"] > 0:
            print("Text Has Bad Words")
            return True
        elif "bad_words_total" not in result:
            print("Cannot determine if text has bad words, maybe an API issue")
            return True
        else:
            return False
    except:
        print("Cannot determine if text has bad words, maybe an API issue")
        return True


try:
    print("Press CTRL-C to stop")
    run()
except KeyboardInterrupt:
    print("Exiting\n")
    sys.exit(0)