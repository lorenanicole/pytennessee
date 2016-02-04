import csv
from serializers import UberDurationEstimate, UberTimeEstimate
import datetime
import pylab

all_duration = []
all_eta = []

with open("/Users/lorenamesa/Desktop/pytennessee/uber_duration_data.csv", "r") as csvdata:
    headers = ['starting_long', 'ending_long', 'high_estimate', 'surge_multiplier', 'starting_lat', 'low_estimate', 'request_id', 'duration', 'localized_display_name', 'ending_lat']
    reader = csv.reader(csvdata)

    for row in reader:
        data = dict(zip(headers, row))
        duration = UberDurationEstimate(**data)
        all_duration.append(duration)
        # print duration.surge
        # print datetime.datetime.fromtimestamp(float(weather.local_epoch)), weather.weather, weather.feels_like

    surging = set([float(duration.surge) for duration in all_duration])
    surging = [float(duration.surge) for duration in all_duration if duration.starting_lat == "41.908511" and duration.type == "uberX"]

    # print len(surging) # 160
    pylab.figure()
    data = pylab.hist(surging, bins=6)

    pylab.title("Range of UberX Surging Rates in January 2016 From Home to Work Between 6am to 12pm")
    pylab.legend(loc='best')
    pylab.xlabel("Surging Rate")
    pylab.ylabel("Number of UberXs")
    pylab.plot()
    pylab.show()

    ranges = list(data[1][0:7])
    categories = []
    num_categories = []

    for num in xrange(len(ranges)-1):
        categories.append(str(ranges[num]) + " to " + str(ranges[num+1]))

    for num in xrange(len(ranges)-1):
        num_categories.append([ranges[num],ranges[num+1]])
    print num_categories
    print categories  # ['1.0 to 1.1', '1.1 to 1.2', '1.2 to 1.3', '1.3 to 1.4', '1.4 to 1.5', '1.5 to 1.6']

    counter = 0

    uberX_surging = [duration for duration in all_duration if duration.starting_lat == "41.908511" and duration.type == "uberX"]

    for uberX in uberX_surging:
        for category in num_categories:
            if category[0] < float(uberX.surge) < category[1]:
                uberX.surge = str(category[0]) + " to " + str(category[1])
                break



with open("/Users/lorenamesa/Desktop/pytennessee/uber_eta_data.csv", "r") as csvdata:
    headers = ['starting_long', 'estimate', 'localized_display_name', 'starting_lat', 'request_id']
    reader = csv.reader(csvdata)

    for row in reader:
        data = dict(zip(headers, row))
        duration = UberTimeEstimate(**data)
        all_eta.append(duration)

    # surging = set([duration.weather for duration in all_duration])
    etas = [float(eta.estimate) / 60 for eta in all_eta if eta.starting_lat == "41.908511" and eta.type == "uberX"]
    uberX_etas = [eta for eta in all_eta if eta.starting_lat == "41.908511" and eta.type == "uberX"]

    for uberX_eta in uberX_etas:
        uberX_eta.estimate = float(uberX_eta.estimate) / 60

    # print len(etas) # 160
    pylab.figure()
    data = pylab.hist(etas, bins=6)

    pylab.title("Range of Uber ETAs in January 2016 From Home to Work Between 6am to 12pm")
    pylab.legend(loc='best')
    pylab.xlabel("Minutes Until Pickup")
    pylab.ylabel("Number of Ubers")
    pylab.plot()
    pylab.show()

    ranges = list(data[1][0:7])
    categories = []
    num_categories = []

    for num in xrange(len(ranges)-1):
        categories.append(str(ranges[num]) + " to " + str(ranges[num+1]))

    for num in xrange(len(ranges)-1):
        num_categories.append([ranges[num], ranges[num+1]])
    print num_categories
    print categories  # ['2.0 to 3.5', '3.5 to 5.0', '5.0 to 6.5', '6.5 to 8.0', '8.0 to 9.5', '9.5 to 11.0']

    # counter = 0
    for uberX_eta in uberX_etas:
        for category in num_categories:
            if category[0] < uberX_eta.estimate < category[1]:
                uberX_eta.estimate = str(category[0]) + " to " + str(category[1])
                break

with open("/Users/lorenamesa/Desktop/pytennessee/uberx_morning_labeled_data.csv", "w") as csvdata:
    headers = ['request_id', 'surge_rate', 'eta']

    uberX_requests = {}
    for uberX in uberX_surging:
        # if uberX_requests.get(uberX.request_id):
            # uberX_requests[uberX.request_id].append({"surging": uberX})
        # else:
        uberX_requests[uberX.request_id] = {"surge_rate": uberX}

    for uberX in uberX_etas:
        if uberX_requests.get(uberX.request_id):
            uberX_requests[uberX.request_id]["eta"] = uberX
        else:
            uberX_requests[uberX.request_id] = {"eta": uberX}

    writer = csv.writer(csvdata, dialect='excel')
    writer.writerow(headers)

    for uberX_request, data in uberX_requests.iteritems():
            writer.writerow([uberX_request, data.get("surge_rate").surge, data.get("eta").estimate])



