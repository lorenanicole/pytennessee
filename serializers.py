from json import JSONEncoder


class Prediction(object):
    def __init__(self, **kwargs):
        self.stop_name = kwargs.get("stpnm")
        self.route = kwargs.get("rt")
        self.route_direction = kwargs.get("rtdir")
        self.arrival_time = kwargs.get("prdtm")
        self.distance_to_stop = int(kwargs.get("dstp", 0))

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__