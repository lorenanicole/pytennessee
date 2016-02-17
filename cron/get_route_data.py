#!/usr/bin/env python

import csv
import sys
import logging

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

sys.path.append('/Users/lorenamesa/Desktop/pyten/lib/python2.7/site-packages/')

from api.cta_api import CTABustracker, CTATraintracker

bus_tracker = CTABustracker()
predictions = bus_tracker.get_predictions_for_stops(route_id=72, stp_id="890,944")
cali_predictions = bus_tracker.get_predictions_for_stops(route_id=52, stp_id="3183,3006")
with open("/Users/lorenamesa/Desktop/pytennessee/bus_data.csv", "ab") as csvdata:
    headers = ['distance_to_stop', 'route', 'vehicle_id', 'arrival_time', 'requested_time', 'route_direction', 'stop_name']

    if predictions:
        logging.info("Writing data for bus data...")
        wr = csv.writer(csvdata, dialect='excel')
        for prediction in predictions:
            wr.writerow(prediction.__dict__.values())
        for cali_p in cali_predictions:
            wr.writerow(cali_p.__dict__.values())  # ['distance_to_stop', 'route', 'vehicle_id', 'arrival_time', 'requested_time', 'route_direction', 'stop_name']


train_tracker = CTATraintracker()
train_predictions = train_tracker.get_predictions_for_stops(stp_id="30112,30116,30153",max=10)

with open("/Users/lorenamesa/Desktop/pytennessee/train_data.csv", "ab") as traindata:
    if train_predictions:
        wr = csv.writer(traindata, dialect='excel')
        logging.info("Writing data for cta data...")
        for prediction in train_predictions:
            wr.writerow(prediction.__dict__.values())
            # "('is_delayed', u'0')","('route', u'Blue')","('is_fault', u'0')","('arrival_time', u'20160124 13:35:50')","('requested_time', u'20160124 13:23:50')","('is_scheduled', u'0')","('stop_name', u'Monroe')","('is_approached', u'0')","('train_direction', u'1')"
