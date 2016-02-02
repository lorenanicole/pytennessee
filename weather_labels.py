import csv
from serializers import CurrentWeather
import datetime
import pylab

all_weather = []

with open("/Users/lorenamesa/Desktop/pytennessee/weather_data_example.csv", "r") as csvdata:
    headers = "windchill,temp,local_epoch,wind_display,weather,location,percipitation_within_hr,feelslike_f,temp_display".split(",")
    reader = csv.reader(csvdata)

    for row in reader:
        data = dict(zip(headers, row))
        weather = CurrentWeather(**data)
        all_weather.append(weather)
        # print datetime.datetime.fromtimestamp(float(weather.local_epoch)), weather.weather, weather.feels_like

    unique_weather = set([weather.weather for weather in all_weather])
    feels_like = [int(weather.feels_like) for weather in all_weather]
    pylab.figure()
    pylab.hist(feels_like, bins = 6)
    pylab.plot()