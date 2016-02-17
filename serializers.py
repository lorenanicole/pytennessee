from json import JSONEncoder
import time
from datetime import datetime
from dateutil import tz

class CTATimeMixin(object):
    def from_timestring_to_utctimestamp(self, timestamp, type=None):

        # Sigh, TrainPredictions include seconds, BusPredictions don't
        if type == 'train':
            timestr_format = "%Y%m%d %H:%M:%S"
        else:
            timestr_format = "%Y%m%d %H:%M"

        local_datetime = datetime.strptime(timestamp, timestr_format).replace(tzinfo=tz.tzlocal())
        return (local_datetime - datetime(1970, 1, 1, tzinfo=tz.tzutc())).total_seconds()

    def set_eta(self):
        return (self.arrival_time - self.requested_time) / 60

    def get_requested_time_hr(self):
        return datetime.fromtimestamp(self.requested_time).replace(tzinfo=tz.tzlocal()).hour

class BusPrediction(CTATimeMixin):
    def __init__(self, **kwargs):
        self.stop_name = kwargs.get("stpnm")
        self.route = kwargs.get("rt")
        self.direction = kwargs.get("rtdir")
        self.arrival_time = self.from_timestring_to_utctimestamp(kwargs.get("prdtm"), type='bus')
        self.distance = int(kwargs.get("dstp", 0))
        self.requested_time = kwargs.get('requested_time')  # self.from_timestring_to_utctimestamp(kwargs.get("tmstmp"), type='bus')
        self.vehicle_id = kwargs.get("vid")
        self.eta = self.set_eta()

    # def get_requested_time_hour(self):
    #     self.from_timestring_to_utctimestamp()
    #     return int(datetime.fromtimestamp(self.requested_time).replace(tzinfo=tz.tzlocal()).hour)

class TrainPrediction(CTATimeMixin):
    def __init__(self, **kwargs):
        self.stop_name = kwargs.get("staNm")
        self.route = kwargs.get("rt")
        self.direction = kwargs.get("trDr")
        self.arrival_time = self.from_timestring_to_utctimestamp(kwargs.get("arrT"), type='train')
        self.requested_time = kwargs.get('requested_time')  # self.from_timestring_to_utctimestamp(kwargs.get("prdt"), type='train')
        self.delayed = kwargs.get("isDly")
        self.scheduled = kwargs.get("isSch")
        self.approaching = kwargs.get("isApp")
        self.fault = kwargs.get("isFlt")
        self.eta = self.set_eta()

class Bulletin(object):
    def __init__(self, **kwargs):
        self.utc_requested_time = int(time.time())  # Utc timestamp
        self.name = kwargs.get("nm")
        self.subject = kwargs.get("sbj")
        self.detail = kwargs.get("dtly")
        self.priority = kwargs.get("prty")
        self.route = kwargs.get("srvc").get("rt") if kwargs.get("srvc") else "N/A"

class UberTimeEstimate(object):
    def __init__(self, requested_time, lat, long, **kwargs):
        self.type = kwargs.get("localized_display_name") # or type
        self.eta = int(kwargs.get("estimate")) / 60
        self.requested_time = requested_time
        self.lat = lat  # starting_lat
        self.long = long  # starting_long

    def set_requested_time(self, utctimestamp):
        self.requested_time = utctimestamp

    def get_requested_time_hr(self):
        return datetime.fromtimestamp(self.requested_time).replace(tzinfo=tz.tzlocal()).hour


class UberDurationEstimate(object):
    def __init__(self, requested_time, lat, long, ending_lat, ending_long, **kwargs):
        self.type = kwargs.get("localized_display_name")
        self.duration = kwargs.get("duration")
        self.high_estimate = kwargs.get("high_estimate", 0)
        self.low_estimate = kwargs.get("low_estimate", 0)
        self.surge = kwargs.get("surge_multiplier")
        # self.distance = kwargs.get("distance")
        self.requested_time = requested_time
        self.lat = lat
        self.long = long
        self.ending_lat = ending_lat
        self.ending_long = ending_long

    def set_requested_time(self, utctimestamp):
        self.requested_time = utctimestamp

    def get_requested_time_hr(self):
        return datetime.fromtimestamp(self.requested_time).replace(tzinfo=tz.tzlocal()).hour


class Tweet(object):
    def __init__(self, requested_time, **kwargs):
        self.requested_time = requested_time
        self.tweet_id = kwargs.get("id_str")
        self.text = kwargs.get("text")
        self.created_at = kwargs.get("created_at")

class CurrentWeather(object):
    def __init__(self, requested_time, **kwargs):
        self.requested_time = requested_time # kwargs.get("local_epoch")  # Local time observed
        self.location = kwargs.get("display_location").get("full") if kwargs.get("display_location") else "N/A"
        self.temperature = kwargs.get("temp_f")
        self.feels_like = kwargs.get("feelslike_f")
        self.weather = kwargs.get("weather")
        self.windchill = kwargs.get("windchill_f")
        self.percipitation_within_hour = kwargs.get("precip_1hr_in")

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__