#!/usr/bin/env python

import csv
import logging
import sys
import uuid
from datetime import datetime

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

sys.path.append('/Users/lorenamesa/Desktop/pyten/lib/python2.7/site-packages/')

from api.uber_api import Uber

uber = Uber()
request_id = uuid.uuid1()

if 6 < datetime.now().hour < 12:
    logger.info("Request ID: " + str(request_id) + " running for morning work uber")
    uber_eta_predictions = uber.get_ride_arrival_time(requested_time=41.908511, starting_lat=41.908511,
                                                      starting_long=-87.696287)
    uber_duration_predictions = uber.get_ride_duration_and_price(requested_time=41.908511, starting_lat=41.908511,
                                                                 starting_long=-87.696287, ending_lat=41.879931,
                                                                 ending_long=-87.629024)
elif 15 < datetime.now().hour < 20:
    logger.info("Request ID: " + str(request_id) + " running for afternoon work uber")
    uber_eta_predictions = uber.get_ride_arrival_time(requested_time=41.879931, starting_lat=41.879931,
                                                      starting_long=-87.629024)
    uber_duration_predictions = uber.get_ride_duration_and_price(requested_time=41.879931, starting_lat=41.879931,
                                                                 starting_long=-87.629024, ending_lat=41.908511,
                                                                 ending_long=-87.696287)

with open("/Users/lorenamesa/Desktop/pytennessee/uber_eta_data.csv", "ab") as csvdata:
    if uber_eta_predictions:
        logging.info("Writing eta for uber data...")
        wr = csv.writer(csvdata, dialect='excel')
        for uber_eta in uber_eta_predictions:
            # print uber_eta.__dict__.keys()
            wr.writerow(uber_eta.__dict__.values()) # ['starting_long', 'estimate', 'type', 'starting_lat', 'request_id']

with open("/Users/lorenamesa/Desktop/pytennessee/uber_duration_data.csv", "ab") as durationcsv:
    if uber_duration_predictions:
        logging.info("Writing price and time for uber data...")
        wr_two = csv.writer(durationcsv, dialect='excel')
        for uber_duration in uber_duration_predictions:
            # print uber_duration.__dict__.keys()
            wr_two.writerow(uber_duration.__dict__.values()) # ['starting_long', 'ending_long', 'high_estimate', 'surge', 'starting_lat', 'low_estimate', 'request_id', 'duration', 'type', 'ending_lat']
