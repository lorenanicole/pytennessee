#!/usr/bin/env python

import csv
import logging
import sys
from weather_underground_api import WeatherUnderground

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

sys.path.append('/Users/lorenamesa/Desktop/pyten/lib/python2.7/site-packages/')

weather_underground = WeatherUnderground(key=None)

current_weather = weather_underground.get_current_weather_for_city(city="Chicago", state="IL")

with open("/Users/lorenamesa/Desktop/pytennessee/weather_data.csv", "ab") as csvdata:
    if current_weather:
        logging.info("Writing weather data...")
        wr = csv.writer(csvdata, dialect='excel')
        wr.writerow(current_weather.__dict__.values())  # windchill,temp,local_epoch,wind_display,weather,location,percipitation_within_hr,feels_like,temp_display