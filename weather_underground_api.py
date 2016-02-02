import json
import requests
from serializers import CurrentWeather
from settings import WEATHER_UNDERGROUND_KEY


class WeatherUnderground(object):
    BASE_URL = "http://api.wunderground.com/api/{0}/"
    def __init__(self, key):
        self.key = key or WEATHER_UNDERGROUND_KEY

    def get_current_weather_for_city(self, city, state):
        request_url = self.BASE_URL.format(self.key) + "conditions/q/{0}/{1}.json".format(state, city)
        return CurrentWeather(**json.loads(requests.get(request_url).content).get("current_observation"))