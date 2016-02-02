import requests
import logging
from logging.config import fileConfig
import xmltodict
from serializers import BusPrediction, TrainPrediction, Bulletin

from settings import CTA_BUSTRACKER_KEY, CTA_TRAINTRACKER_KEY

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
            return [BusPrediction(**prediction) for prediction in xmltodict.parse(response.content).get("bustime-response").get("prd")]
        except Exception as e:
            logger.info("Exception: " + str(e.message))

    def get_bulletins(self, route_id=None, stp_id=None):
        base_url = "http://www.ctabustracker.com/bustime/api/v1/getservicebulletins?key={0}"

        # http://www.ctabustracker.com/bustime/api/v1/getservicebulletins?key=T6ketWk5cWetPgYVqkvEVJVng&stpid=890,944,3183,3006
        if stp_id:
            response = requests.get(base_url.format(self.key) + "&stpid={0}".format(stp_id))
            return [Bulletin(**bulletin) for bulletin in xmltodict.parse(response.content).get("bustime-response").get("sb")]
        elif route_id:
            response = requests.get(base_url.format(self.key) +"&rt={0}".format(route_id))
            return [Bulletin(**bulletin) for bulletin in xmltodict.parse(response.content).get("bustime-response").get("sb")]

class CTATraintracker(object):
    def __init__(self, key=None):
        self.key = key or CTA_TRAINTRACKER_KEY

    def get_predictions_for_stops(self, stp_id, max=10):
        base_url = "http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key={0}&stpid={1}&max={2}"
        try:
            response = requests.get(base_url.format(self.key, stp_id, max))
            return [TrainPrediction(**prediction) for prediction in xmltodict.parse(response.content).get("ctatt").get("eta")]
        except Exception as e:
            logger.info("Exception: " + str(e.message))