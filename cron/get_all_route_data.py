#!/usr/bin/env python

__author__ = 'lorenamesa'

import sys
import logging
import records
import os
import time

'''
* * * * * cd /Users/lorenamesa/Desktop/pytennessee/cron/get_all_route_data.py
'''

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

sys.path.append('/usr/local/lib/python2.7/site-packages')

logger.info("path added: {0}".format(os.path.abspath(os.path.dirname(__file__) + '/' + '../')))

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../'))

from api.cta_api import CTABustracker, CTATraintracker
from api.uber_api import Uber
from sqlalchemy.exc import IntegrityError
from api.twitter_api import Twitter
from api.weather_underground_api import WeatherUnderground

db = records.Database("sqlite:////Users/lorenamesa/Desktop/pytennessee/pytennessee.db")


requested_time = int(time.time())

bus_tracker = CTABustracker()
predictions = bus_tracker.get_predictions_for_stops(requested_time=requested_time, route_id=72, stp_id="890,944")
cali_predictions = bus_tracker.get_predictions_for_stops(requested_time=requested_time, route_id=52, stp_id="3183,3006")

if predictions:
    logging.info("Writing bus data...")

    for prediction in predictions:
        db.query("INSERT INTO bus_predictions " +
                 "(stop_name, route, direction, arrival_time, requested_time, distance, vehicle_id, eta) " +
                 "VALUES ('{0}', '{1}', '{2}', {3}, {4}, {5}, {6}, {7})".format(prediction.stop_name,
                                                                                prediction.route,
                                                                                prediction.direction,
                                                                                prediction.arrival_time,
                                                                                prediction.requested_time,
                                                                                prediction.distance,
                                                                                prediction.vehicle_id,
                                                                                prediction.eta))
    for cali_p in cali_predictions:
        db.query("INSERT INTO bus_predictions " +
                 "(stop_name, route, direction, arrival_time, requested_time, distance, vehicle_id, eta) " +
                 "VALUES ('{0}', '{1}', '{2}', {3}, {4}, {5}, {6}, {7})".format(prediction.stop_name,
                                                                                prediction.route,
                                                                                prediction.direction,
                                                                                prediction.arrival_time,
                                                                                prediction.requested_time,
                                                                                prediction.distance,
                                                                                prediction.vehicle_id,
                                                                                prediction.eta))



train_tracker = CTATraintracker()
train_predictions = train_tracker.get_predictions_for_stops(requested_time=requested_time, stp_id="30112,30116,30153", max=10)

if train_predictions:
    logging.info("Writing cta data...")
    for prediction in train_predictions:
        db.query("INSERT INTO train_predictions " +
         "(stop_name, route, direction, arrival_time, requested_time, delayed, scheduled, approaching, fault, eta) " +
         "VALUES ('{0}', '{1}', '{2}', {3}, {4}, {5}, {6}, {7}, {8}, {9})".format(prediction.stop_name,
                                                                                  prediction.route,
                                                                                  prediction.direction,
                                                                                  prediction.arrival_time,
                                                                                  prediction.requested_time,
                                                                                  prediction.delayed,
                                                                                  prediction.scheduled,
                                                                                  prediction.approaching,
                                                                                  prediction.fault,
                                                                                  prediction.eta))

uber = Uber()



morning_uber_eta_predictions = uber.get_ride_arrival_time(requested_time=requested_time, lat=41.908511, long=-87.696287)
morning_uber_duration_predictions = uber.get_ride_duration_and_price(requested_time=requested_time, lat=41.908511,
                                                                     long=-87.696287, ending_lat=41.879931,
                                                                     ending_long=-87.629024)

evening_uber_eta_predictions = uber.get_ride_arrival_time(requested_time=requested_time, lat=41.879931, long=-87.629024)
evening_uber_duration_predictions = uber.get_ride_duration_and_price(requested_time=requested_time, lat=41.879931,
                                                                     long=-87.629024, ending_lat=41.908511,
                                                                     ending_long=-87.696287)

all_uber_eta_predictions = morning_uber_eta_predictions + evening_uber_eta_predictions
all_uber_duration_predictions = morning_uber_duration_predictions + evening_uber_duration_predictions

if all_uber_eta_predictions:
    logging.info("Writing uber eta data...")
    for prediction in all_uber_eta_predictions:
        db.query("INSERT INTO uber_predictions " +
         "(type, requested_time, lat, long, eta) " +
         "VALUES ('{0}', {1}, {2}, {3}, {4})".format(prediction.type,
                                                     prediction.requested_time,
                                                     prediction.lat,
                                                     prediction.long,
                                                     prediction.eta))

if all_uber_duration_predictions:
    logging.info("Writing uber duration data...")
    for prediction in all_uber_duration_predictions:
        db.query("INSERT INTO uber_durations " +
         "(requested_time, type, duration, surge, low_estimate, high_estimate, lat, long, end_lat, end_long) " +
         "VALUES ({0}, '{1}', {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9})".format(prediction.requested_time,
                                                                              prediction.type,
                                                                              prediction.duration,
                                                                              prediction.surge,
                                                                              prediction.low_estimate or 0,
                                                                              prediction.high_estimate or 0,
                                                                              prediction.lat,
                                                                              prediction.long,
                                                                              prediction.ending_lat,
                                                                              prediction.ending_long))

twitter = Twitter()

user_timeline = twitter.get_user_timeline(requested_time=requested_time, user_id=None, screen_name="cta")

if user_timeline:
    logging.info("Writing tweets for cta timeline data...")

    for tweet in user_timeline:
        try:
            db.query("INSERT INTO tweets (requested_time, tweet_id, text, created_at) " +
             'VALUES ({0}, {1}, "{2}", "{3}")'.format(tweet.requested_time,
                                                    tweet.tweet_id,
                                                    tweet.text,
                                                    tweet.created_at))
        except IntegrityError as e:
            logger.info("Skipping tweet_id {0} already in DB".format(tweet.tweet_id))

weather_underground = WeatherUnderground(key=None)

current_weather = weather_underground.get_current_weather_for_city(requested_time=requested_time, city="Chicago", state="IL")

if current_weather:
    logging.info("Writing weather data...")

    db.query("INSERT INTO weather (requested_time, location, temperature, feels_like, weather, windchill, percipitation_within_hour) " +
             "VALUES ({0}, '{1}', {2}, {3}, '{4}', '{5}', '{6}')".format(current_weather.requested_time,
                                                                         current_weather.location,
                                                                         current_weather.temperature,
                                                                         current_weather.feels_like,
                                                                         current_weather.weather,
                                                                         current_weather.windchill,
                                                                         current_weather.percipitation_within_hour))