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


from api.cta_api import CTABustracker

bus_tracker = CTABustracker("T6ketWk5cWetPgYVqkvEVJVng")
bulletins = bus_tracker.get_bulletins(stp_id="890,944,3183,3006")

with open("/Users/lorenamesa/Desktop/pytennessee/bus_service_bulletins.csv", "ab") as csvdata:
    if bulletins:
        logging.info("Writing service bulletins for bus data...")
        wr = csv.writer(csvdata, dialect='excel')
        for bulletin in bulletins:
            wr.writerow(bulletin.__dict__.values())