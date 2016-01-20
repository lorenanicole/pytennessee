import requests
import logging
from logging.config import fileConfig
import xmltodict
import json
from serializers import Prediction

from settings import CTA_BUSTRACKER_KEY

# fileConfig('logging_config.ini')
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class CTABustracker(object):
    def __init__(self, key=None):
        self.key = key or CTA_BUSTRACKER_KEY

    def get_stop_on_route_predictions(self, route_id, stp_id, top=3):
        base_url = "http://www.ctabustracker.com/bustime/api/v1/getpredictions?key={0}&rt={1}&stpid={2}&top={3}"
        try:
            response = requests.get(base_url.format(self.key, route_id, stp_id, top))
            return [Prediction(**prediction) for prediction in xmltodict.parse(response.content).get("bustime-response").get("prd")]
        except Exception as e:
            logger.info("Exception: " + e.message)
