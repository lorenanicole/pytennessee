import csv
from serializers import TrainPrediction
from datetime import datetime
import pylab
from dateutil import tz

all_train = []

with open("/Users/lorenamesa/Desktop/pytennessee/train_data.csv", "r") as csvdata:
    headers = ['isDly','rt','isFlt','arrT','prdt','is_scheduled','staNm','is_approached','trDr']
    reader = csv.reader(csvdata)

    for row in reader:
        data = dict(zip(headers, row))
        train_p = TrainPrediction(**data)
        all_train.append(train_p)
        print datetime.strptime(train_p.arrival_time, "%Y%m%d %H:%M:%S")
        local_datetime = datetime.strptime(train_p.arrival_time, "%Y%m%d %H:%M:%S").replace(tzinfo=tz.tzlocal())
        train_p.requested_time = int((local_datetime - datetime(1970, 1, 1, tzinfo=tz.tzutc())).total_seconds())
        print train_p.get_requested_time_hr()
        print train_p.requested_time

        # print datetime.datetime.strptime(bus_prediction.arrival_time, "%Y%m%d %H:%M")  # local time
        # print bus_prediction.get_requested_time_hr()

    etas = [int(train_eta.train_eta) for train_eta in all_train if 6 < train_eta.get_requested_time_hr() < 12 and train_eta.stop_name == 'Damen']
    north_ave_etas = [train_eta for train_eta in all_train if 6 < train_eta.get_requested_time_hr() < 12 and train_eta.stop_name == 'Damen']

    print len(etas)  # 589
    pylab.figure()
    data = pylab.hist(etas, bins=6)

    pylab.title("Range of Damen Blue Line Train ETAs in January 2016 From Home to Work Between 6am to 12pm")
    pylab.legend(loc='best')
    pylab.xlabel("Minutes Until Arrival")
    pylab.ylabel("Number of Trains")
    pylab.plot()
    pylab.show()

    # pylab.title("Range of Damen Blue Line Train ETAs in January 2016 From Home to Work Between 6am to 12pm")
    # pylab.legend(loc='best')
    # pylab.xlabel("Train Delayed")
    # pylab.ylabel("Number of Trains")
    # pylab.plot()
    # pylab.show()

    ranges = list(data[1][0:7])
    categories = []  # ['1.0 to 5.5', '5.5 to 10.0', '10.0 to 14.5', '14.5 to 19.0', '19.0 to 23.5', '23.5 to 28.0']
    num_categories = []

    for num in xrange(len(ranges)-1):
        categories.append(str(ranges[num]) + " to " + str(ranges[num+1]))

    for num in xrange(len(ranges)-1):
        num_categories.append([ranges[num], ranges[num+1]])
    print num_categories
    print categories  #

    for train_p in north_ave_etas:
        for category in num_categories:
            if category[0] < float(train_p.train_eta) < category[1]:
                train_p.train_eta = str(category[0]) + " to " + str(category[1])
                break

    cali_etas = [train_eta.train_eta for train_eta in all_train if 6 < train_eta.get_requested_time_hr() < 12 and train_eta.stop_name == 'California']
    cali_st_etas = [train_eta for train_eta in all_train if 6 < train_eta.get_requested_time_hr() < 12 and train_eta.stop_name == 'California']

    print len(cali_st_etas)  # 718
    pylab.figure()
    data = pylab.hist(cali_etas, bins=6)

    pylab.title("Range of California Blue Line Train ETAs in January 2016 From Home to Work Between 6am to 12pm")
    pylab.legend(loc='best')
    pylab.xlabel("Minutes Until Arrival")
    pylab.ylabel("Number of Trains")
    pylab.plot()
    pylab.show()

    ranges = list(data[1][0:7])
    categories = []  # ['1.0 to 4.5', '4.5 to 8.0', '8.0 to 11.5', '11.5 to 15.0', '15.0 to 18.5', '18.5 to 22.0']
    num_categories = []

    for num in xrange(len(ranges)-1):
        categories.append(str(ranges[num]) + " to " + str(ranges[num+1]))

    for num in xrange(len(ranges)-1):
        num_categories.append([ranges[num], ranges[num+1]])
    print num_categories
    print categories  #

    for train_p in cali_st_etas:
        for category in num_categories:
            if category[0] < float(train_p.train_eta) < category[1]:
                train_p.train_eta = str(category[0]) + " to " + str(category[1])
                break

with open("/Users/lorenamesa/Desktop/pytennessee/train_labeled_data.csv", "w") as csvdata:
    headers = ['requested_time', 'route', 'direction', 'stop_name', 'eta', 'delayed']

    writer = csv.writer(csvdata, dialect='excel')
    writer.writerow(headers)
    count = 0
    for train_p in north_ave_etas:
            writer.writerow([train_p.requested_time, train_p.route, train_p.train_direction,
                             train_p.stop_name, train_p.train_eta, train_p.is_delayed])
            # if int(train_p.is_fault) == 1:
            #     count += 1

    for train_p in cali_st_etas:
            writer.writerow([train_p.requested_time, train_p.route, train_p.train_direction,
                             train_p.stop_name, train_p.train_eta, train_p.is_delayed])
            # if int(train_p.is_fault) == 1:
            #     count += 1

print "trains late: ", count  # None? For both is_fault and is_delayed (>.<)

