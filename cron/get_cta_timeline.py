#!/usr/bin/env python

import csv
import logging
import sys

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

sys.path.append('/Users/lorenamesa/Desktop/pyten/lib/python2.7/site-packages/')

from api.twitter_api import Twitter

twitter = Twitter()

user_timeline = twitter.get_user_timeline(user_id=None, screen_name="cta")

with open("/Users/lorenamesa/Desktop/pytennessee/cta_tweet_data.csv", "ab") as csvdata:
    if user_timeline:
        logging.info("Writing tweets for cta timeline data...")
        wr = csv.writer(csvdata, dialect='excel')
        for tweet in user_timeline:
            print tweet.__dict__.keys()  # ['tweet_id', 'created_at', 'text']
            wr.writerow(tweet.__dict__.values())