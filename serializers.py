from json import JSONEncoder
import time
from datetime import datetime
from dateutil import tz


class BusPrediction(object):
    def __init__(self, **kwargs):
        self.stop_name = kwargs.get("stpnm")
        self.route = kwargs.get("rt")
        self.route_direction = kwargs.get("rtdir")
        self.arrival_time = kwargs.get("prdtm")
        self.distance_to_stop = int(kwargs.get("dstp", 0))
        self.requested_time = kwargs.get("tmstmp")
        self.vehicle_id = kwargs.get("vid")
        self.bus_eta = self.set_bus_eta()

    def set_bus_eta(self):
        return (datetime.strptime(self.arrival_time, "%Y%m%d %H:%M") -
               datetime.strptime(self.requested_time, "%Y%m%d %H:%M")).seconds / 60.0

    def get_requested_time_hr(self):
        return datetime.fromtimestamp(self.requested_time).replace(tzinfo=tz.tzlocal()).hour

class Bulletin(object):
    def __init__(self, **kwargs):
        self.utc_requested_time = int(time.time())  # Utc timestamp
        self.name = kwargs.get("nm")
        self.subject = kwargs.get("sbj")
        self.detail = kwargs.get("dtly")
        self.priority = kwargs.get("prty")
        self.route = kwargs.get("srvc").get("rt") if kwargs.get("srvc") else "N/A"

class TrainPrediction(object):
    def __init__(self, **kwargs):
        self.stop_name = kwargs.get("staNm")
        self.route = kwargs.get("rt")
        self.train_direction = kwargs.get("trDr")
        self.arrival_time = kwargs.get("arrT")
        self.requested_time = kwargs.get("prdt")
        self.is_delayed = kwargs.get("isDly")
        self.is_scheduled = kwargs.get("isSch")
        self.is_approaching = kwargs.get("isApp")
        self.is_fault = kwargs.get("isFlt")
        self.train_eta = self.set_train_eta()

    def set_train_eta(self):
        return (datetime.strptime(self.arrival_time, "%Y%m%d %H:%M:%S") -
               datetime.strptime(self.requested_time, "%Y%m%d %H:%M:%S")).seconds / 60.0

    def get_requested_time_hr(self):
        return datetime.fromtimestamp(self.requested_time).replace(tzinfo=tz.tzlocal()).hour

class UberTimeEstimate(object):
    def __init__(self, request_id, starting_lat, starting_long, **kwargs):
        self.type = kwargs.get("localized_display_name") # or type
        self.estimate = kwargs.get("estimate")
        self.request_id = request_id
        self.starting_lat = starting_lat
        self.starting_long = starting_long

    def set_requested_time(self, utctimestamp):
        self.requested_time = utctimestamp

    def get_requested_time_hr(self):
        return datetime.fromtimestamp(self.requested_time).replace(tzinfo=tz.tzlocal()).hour


class UberDurationEstimate(object):
    def __init__(self, request_id, starting_lat, starting_long, ending_lat, ending_long, **kwargs):
        self.type = kwargs.get("localized_display_name")
        self.duration = kwargs.get("duration")
        self.high_estimate = kwargs.get("high_estimate")
        self.low_estimate = kwargs.get("high_estimate")
        self.surge = kwargs.get("surge_multiplier")
        # self.distance = kwargs.get("distance")
        self.request_id = request_id
        self.starting_lat = starting_lat
        self.starting_long = starting_long
        self.ending_lat = ending_lat
        self.ending_long = ending_long

    def set_requested_time(self, utctimestamp):
        self.requested_time = utctimestamp

    def get_requested_time_hr(self):
        return datetime.fromtimestamp(self.requested_time).replace(tzinfo=tz.tzlocal()).hour


class Tweet(object):
    def __init__(self, **kwargs):
        self.tweet_id = kwargs.get("id_str")
        self.text = kwargs.get("text")
        self.created_at = kwargs.get("created_at")

class CurrentWeather(object):
    def __init__(self, **kwargs):
        self.local_epoch = kwargs.get("local_epoch")  # Local time observed
        self.location = kwargs.get("display_location").get("full") if kwargs.get("display_location") else "N/A"
        self.temp = kwargs.get("temp_f")
        self.temp_display = kwargs.get("temperature_string")
        self.feels_like = kwargs.get("feelslike_f")
        self.weather = kwargs.get("weather")
        self.wind_display = kwargs.get("wind_string")
        self.windchill = kwargs.get("windchill_f")
        self.percipitation_within_hr = kwargs.get("precip_1hr_in")

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__