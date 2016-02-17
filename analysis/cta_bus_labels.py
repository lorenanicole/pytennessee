import csv
from serializers import BusPrediction, TrainPrediction
from datetime import datetime
import pylab
from dateutil import tz

all_bus = []

with open("/Users/lorenamesa/Desktop/pytennessee/bus_data.csv", "r") as csvdata:
    headers = ['distance_to_stop', 'rt', 'vehicle_id', 'prdtm', 'tmstmp', 'rtdir', 'stpnm']
    reader = csv.reader(csvdata)

    for row in reader:
        data = dict(zip(headers, row))
        bus_prediction = BusPrediction(**data)
        print datetime.strptime(bus_prediction.arrival_time, "%Y%m%d %H:%M")
        local_datetime = datetime.strptime(bus_prediction.arrival_time, "%Y%m%d %H:%M").replace(tzinfo=tz.tzlocal())
        bus_prediction.requested_time = int((local_datetime - datetime(1970, 1, 1, tzinfo=tz.tzutc())).total_seconds())
        print bus_prediction.get_requested_time_hr()
        print bus_prediction.requested_time
        all_bus.append(bus_prediction)
        # print datetime.datetime.strptime(bus_prediction.arrival_time, "%Y%m%d %H:%M")  # local time
        # print bus_prediction.get_requested_time_hr()

    etas = [int(bus_eta.bus_eta) for bus_eta in all_bus if 6 < bus_eta.get_requested_time_hr() < 12 and bus_eta.stop_name == 'North Ave & California']
    north_ave_etas = [bus_eta for bus_eta in all_bus if 6 < bus_eta.get_requested_time_hr() < 12 and bus_eta.stop_name == 'North Ave & California']

    print len(etas)  # 461


    # eta_hours = [bus_eta.get_requested_time_hr() for bus_eta in all_bus if 6 < bus_eta.get_requested_time_hr() < 12 and bus_eta.stop_name == 'North Ave & California']
    # print set(sorted(eta_hours))
    #
    # n_eta_hours = [bus_eta.get_requested_time_hr() for bus_eta in all_bus if 6 < bus_eta.get_requested_time_hr() < 12 and bus_eta.stop_name == 'California & Le Moyne']
    # print set(sorted(n_eta_hours))

    pylab.figure()
    data = pylab.hist(etas, bins=6)

    pylab.title("Range of North Ave Bus ETAs in January 2016 From Home to Work Between 6am to 12pm")
    pylab.legend(loc='best')
    pylab.xlabel("Minutes Until Pickup")
    pylab.ylabel("Number of Buses")
    pylab.plot()
    # pylab.show()

    ranges = list(data[1][0:7])
    categories = []  # ['0.0 to 5.16666666667', '5.16666666667 to 10.3333333333', '10.3333333333 to 15.5', '15.5 to 20.6666666667', '20.6666666667 to 25.8333333333', '25.8333333333 to 31.0']
    num_categories = []

    for num in xrange(len(ranges)-1):
        categories.append(str(ranges[num]) + " to " + str(ranges[num+1]))

    for num in xrange(len(ranges)-1):
        num_categories.append([ranges[num], ranges[num+1]])
    print num_categories
    print categories  #

    counter = 0
    for bus_prediction in north_ave_etas:
        for category in num_categories:
            if category[0] < float(bus_prediction.bus_eta) < category[1]:
                bus_prediction.bus_eta = str(category[0]) + " to " + str(category[1])
                break

    cali_etas = [bus_eta.bus_eta for bus_eta in all_bus if 6 < bus_eta.get_requested_time_hr() < 12 and bus_eta.stop_name == 'California & Le Moyne']
    cali_st_etas = [bus_eta for bus_eta in all_bus if 6 < bus_eta.get_requested_time_hr() < 12 and bus_eta.stop_name == 'California & Le Moyne']

    print len(cali_st_etas)  # 469
    pylab.figure()
    cali_data = pylab.hist(cali_etas, bins=6)

    pylab.title("Range of California Bus ETAs in January 2016 From Home to Work Between 6am to 12pm")
    pylab.legend(loc='best')
    pylab.xlabel("Minutes Until Pickup")
    pylab.ylabel("Number of Buses")
    pylab.plot()
    # pylab.show()

    cali_ranges = list(cali_data[1][0:7])
    cali_categories = []  # ['0.0 to 5.16666666667', '5.16666666667 to 10.3333333333', '10.3333333333 to 15.5', '15.5 to 20.6666666667', '20.6666666667 to 25.8333333333', '25.8333333333 to 31.0']
    cali_num_categories = []

    for num in xrange(len(cali_ranges)-1):
        cali_categories.append(str(cali_ranges[num]) + " to " + str(cali_ranges[num+1]))

    for num in xrange(len(cali_ranges)-1):
        cali_num_categories.append([cali_ranges[num], cali_ranges[num+1]])
    print cali_num_categories
    print cali_categories  #


    for bus_prediction in cali_st_etas:
        for category in cali_num_categories:
            if category[0] < float(bus_prediction.bus_eta) < category[1]:
                bus_prediction.bus_eta = str(category[0]) + " to " + str(category[1])
                break

with open("/Users/lorenamesa/Desktop/pytennessee/bus_labeled_data.csv", "w") as csvdata:
    headers = ['requested_time', 'route', 'direction', 'stop_name', 'eta', 'delayed']

    writer = csv.writer(csvdata, dialect='excel')
    writer.writerow(headers)

    for bus_prediction in north_ave_etas:
            writer.writerow([bus_prediction.requested_time, bus_prediction.route,
                             bus_prediction.route_direction, bus_prediction.stop_name,
                             bus_prediction.bus_eta, "0"])

    for bus_prediction in cali_st_etas:
            writer.writerow([bus_prediction.requested_time, bus_prediction.route,
                             bus_prediction.route_direction, bus_prediction.stop_name,
                             bus_prediction.bus_eta, "0"])


