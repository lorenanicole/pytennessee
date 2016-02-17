# https://sandbox-api.uber.com/<version>
# /v1/sandbox/requests/
import json
import requests
from requests_oauthlib import OAuth2, OAuth1
from serializers import UberTimeEstimate, UberDurationEstimate
from settings import UBER_CLIENT_ID, UBER_CLIENT_SECRET, UBER_SERVER_TOKEN

class Uber(object):
    SANDBOX_BASE_URL = "https://sandbox-api.uber.com/v1/"  # Version number
    BASE_URL = "https://api.uber.com/v1/"

    def __init__(self, client_id=None, client_secret=None, server_token=None):
        self.client_id = client_id or UBER_CLIENT_ID
        self.client_secret = client_secret or UBER_CLIENT_SECRET
        self.server_token = server_token or UBER_SERVER_TOKEN
        # self.oauth_client = OAuth2(client_id=self.client_id, token=self.server_token)

    def get_ride_arrival_time(self, requested_time, lat, long, product_id=None):
        # /v1/estimates/time
        request_url = self.BASE_URL + "estimates/time?start_latitude={0}&start_longitude={1}".format(lat, long)

        if product_id:  # Allows to choose specific service like UberX
            request_url += "&product_id={0}".format(product_id)

        response_data = requests.get(request_url, headers={"Authorization": "Token {0}".format(self.server_token)}).content

        return [UberTimeEstimate(requested_time=requested_time, lat=lat, long=long, **estimate)
                for estimate in json.loads(response_data).get("times")]

    def get_ride_duration_and_price(self, requested_time, lat, long, ending_lat, ending_long, product=None):
        # /v1/estimates/price
        request_url = self.BASE_URL + "estimates/price?start_latitude={0}&start_longitude={1}&end_latitude={2}&end_longitude={3}"\
            .format(lat, long, ending_lat, ending_long)

        response_data = requests.get(request_url, headers={"Authorization": "Token {0}".format(self.server_token)}).content

        duration_ests = [
            UberDurationEstimate(requested_time=requested_time, lat=lat, long=long,
                                 ending_lat=ending_lat, ending_long=ending_long, **dur_est) for dur_est in json.loads(response_data).get("prices")]

        if product:
            return [dur_est for dur_est in duration_ests if dur_est.type == product ]

        return duration_ests

