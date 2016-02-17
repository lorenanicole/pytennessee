class Route(object):
    def __init__(self, **kwargs):
        self.time_start = kwargs.get('time_start')  # Starting time a user would look for this route
        self.time_stop = kwargs.get('time_stop')  # Ending time a user would look for this route
        self.type = kwargs.get('type')  # UberX, UberTaxi, Train, Bus
        self.location = kwargs.get('location')
        self.destination = kwargs.get('destination')

class User(object):
    def __init__(self, **kwargs):
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')