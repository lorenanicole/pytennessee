import csv
from serializers import UberDurationEstimate, UberTimeEstimate
from datetime import datetime
import pylab
from dateutil import tz

all_duration = []
all_eta = []
all_dates = []
string_dates = []
with open("/Users/lorenamesa/Desktop/pytennessee/uber_jobs.log", "r") as uber_jobs:

    for row in uber_jobs:
        string_date = row[0:16]
        print string_date
        string_dates.append(string_date)
        all_dates.append(datetime.strptime(string_date, "%Y-%m-%d %H:%M").replace(tzinfo=tz.tzlocal()))

# print all_dates

with open("/Users/lorenamesa/Desktop/pytennessee/uber_duration_data.csv", "r") as csvdata:
    headers = ['starting_long', 'ending_long', 'high_estimate', 'surge_multiplier', 'starting_lat', 'low_estimate', 'request_id', 'duration', 'localized_display_name', 'ending_lat']
    reader = csv.reader(csvdata)


    for row in reader:
        data = dict(zip(headers, row))
        duration = UberDurationEstimate(**data,,
        all_duration.append(duration)

    duration_req_ids = set([duration.request_id for duration in all_duration])
    req_id_to_date = dict(zip(duration_req_ids, all_dates))


    all_duration = [d for d in all_duration if d.request_id in req_id_to_date.keys()]
    for duration in all_duration:
        print req_id_to_date[duration.request_id]
        utctimestamp = int((req_id_to_date[duration.request_id] - datetime(1970, 1, 1, tzinfo=tz.tzutc())).total_seconds())
        duration.set_requested_time(utctimestamp)

    uberX_surging = [duration for duration in all_duration if duration.starting_lat == "41.908511" and duration.type == "uberX" and 6 < duration.get_requested_time_hr() < 12]

    # print "Num of duration req ids : ", len(duration_req_ids)

    surging = [float(duration.surge) for duration in uberX_surging]

    print len(surging)  # 117
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
    print categories  # ['1.0 to 1.15', '1.15 to 1.3', '1.3 to 1.45', '1.45 to 1.6', '1.6 to 1.75', '1.75 to 1.9']

    counter = 0

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
        duration = UberTimeEstimate(**data,,
        all_eta.append(duration)

    all_eta = [eta for eta in all_eta if eta.request_id in req_id_to_date.keys()]

    for eta in all_eta:
        eta.estimate = float(eta.estimate) / 60
        utctimestamp = int((req_id_to_date[eta.request_id] - datetime(1970, 1, 1, tzinfo=tz.tzutc())).total_seconds())
        eta.set_requested_time(utctimestamp)

    uberX_etas = [eta for eta in all_eta if eta.starting_lat == "41.908511" and eta.type == "uberX" and 6 < eta.get_requested_time_hr() < 12]
    etas = [eta.estimate for eta in uberX_etas]

    print len(etas)  # 117
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
    headers = ['request_time', 'request_id', 'surge_rate', 'eta']

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
            writer.writerow([data.get("eta").requested_time, uberX_request, data.get("surge_rate").surge, data.get("eta").estimate])


#
