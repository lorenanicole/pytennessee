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

    num_of_hours = [datetime.datetime.fromtimestamp(float(weather.local_epoch)) for weather in all_weather]
    print len(num_of_hours)
    unique_weather = set([weather.weather for weather in all_weather])
    feels_like = [int(weather.feels_like) for weather in all_weather]
    pylab.figure()
    data = pylab.hist(feels_like, bins=6)

    # pylab.title("Range of Temperature in January 2016 By Hour")
    # pylab.legend(loc='best')
    # pylab.xlabel("Temperature")
    # pylab.ylabel("Number of Hours")
    # pylab.plot()
    # pylab.show()

    ranges = list(data[1][0:7])
    categories = []
    num_categories = []

    # for num in xrange(len(ranges)-1):
    #     categories.append(str(ranges[num]) + " to " + str(ranges[num+1]))

    for num in xrange(len(ranges)-1):
        num_categories.append([ranges[num],ranges[num+1]])

    # print categories # ['18.0 to 22.8333333333', '22.8333333333 to 27.6666666667', '27.6666666667 to 32.5', '32.5 to 37.3333333333', '37.3333333333 to 42.1666666667', '42.1666666667 to 47.0']

    counter = 0
    for weather in all_weather:
        for category in num_categories:
            if category[0] < float(weather.feels_like) < category[1]:
                weather.feels_like = str(category[0]) + " to " + str(category[1])
                break

    print unique_weather # set(['Partly Cloudy', 'Clear', 'Overcast', 'Mostly Cloudy', 'Rain'])

with open("/Users/lorenamesa/Desktop/pytennessee/weather_labeled_data.csv", "w") as csvdata:
    headers = ['date', 'weather', 'feels_like']

    writer = csv.writer(csvdata, dialect='excel')
    writer.writerow(headers)

    for weather in all_weather:
            writer.writerow([weather.local_epoch, weather.weather, weather.feels_like])

