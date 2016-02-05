import csv
import json
from dateutil import tz
from datetime import datetime
import pylab

dates = {}
all_data = {}


import csv
from serializers import UberDurationEstimate, UberTimeEstimate, BusPrediction, TrainPrediction
from datetime import datetime
import pylab
from dateutil import tz

'''
Step 1: Break data into features, compile into one file, sort data based on created_at date,
select section with all features present.
'''

# all_duration = []
# all_eta = []
# all_dates = []
# string_dates = []
#
# '''
# Import Uber data
# '''
#
# with open("/Users/lorenamesa/Desktop/pytennessee/uber_jobs.log", "r") as uber_jobs:
#
#     for row in uber_jobs:
#         string_date = row[0:16]
#         string_dates.append(string_date)
#         all_dates.append(datetime.strptime(string_date, "%Y-%m-%d %H:%M").replace(tzinfo=tz.tzlocal()))
#
# with open("/Users/lorenamesa/Desktop/pytennessee/uber_duration_data.csv", "r") as csvdata:
#     headers = ['starting_long', 'ending_long', 'high_estimate', 'surge_multiplier', 'starting_lat', 'low_estimate', 'request_id', 'duration', 'localized_display_name', 'ending_lat']
#     reader = csv.reader(csvdata)
#
#
#     for row in reader:
#         data = dict(zip(headers, row))
#         duration = UberDurationEstimate(**data)
#         all_duration.append(duration)
#
#     duration_req_ids = set([duration.request_id for duration in all_duration])
#     req_id_to_date = dict(zip(duration_req_ids, all_dates))
#
#
#     all_duration = [d for d in all_duration if d.request_id in req_id_to_date.keys()]
#     for duration in all_duration:
#         utctimestamp = int((req_id_to_date[duration.request_id] - datetime(1970, 1, 1, tzinfo=tz.tzutc())).total_seconds())
#         duration.set_requested_time(utctimestamp)
#
#     uberX_surging = [duration for duration in all_duration if duration.starting_lat == "41.908511" and duration.type == "uberX" and 6 < duration.get_requested_time_hr() < 12]
#
#     surging = [float(duration.surge) for duration in uberX_surging]
#
#     print len(surging)  # 117
#
#
# with open("/Users/lorenamesa/Desktop/pytennessee/uber_eta_data.csv", "r") as csvdata:
#     headers = ['starting_long', 'estimate', 'localized_display_name', 'starting_lat', 'request_id']
#     reader = csv.reader(csvdata)
#
#     for row in reader:
#         data = dict(zip(headers, row))
#         duration = UberTimeEstimate(**data)
#         all_eta.append(duration)
#
#     all_eta = [eta for eta in all_eta if eta.request_id in req_id_to_date.keys()]
#
#     for eta in all_eta:
#         eta.estimate = float(eta.estimate) / 60
#         utctimestamp = int((req_id_to_date[eta.request_id] - datetime(1970, 1, 1, tzinfo=tz.tzutc())).total_seconds())
#         eta.set_requested_time(utctimestamp)
#
#     uberX_etas = [eta for eta in all_eta if eta.starting_lat == "41.908511" and eta.type == "uberX" and 6 < eta.get_requested_time_hr() < 12]
#     etas = [eta.estimate for eta in uberX_etas]
#
#     print len(etas)  # 117
#
# '''
# Save compiled uber data
# '''
#
# with open("/Users/lorenamesa/Desktop/pytennessee/uberx_morning_data_nonlabeled.csv", "w") as csvdata:
#     headers = ['request_time', 'request_id', 'surge_rate', 'eta']
#
#     uberX_requests = {}
#     for uberX in uberX_surging:
#         uberX_requests[uberX.request_id] = {"surge_rate": uberX}
#
#     for uberX in uberX_etas:
#         if uberX_requests.get(uberX.request_id):
#             uberX_requests[uberX.request_id]["eta"] = uberX
#         else:
#             uberX_requests[uberX.request_id] = {"eta": uberX}
#
#     writer = csv.writer(csvdata, dialect='excel')
#     writer.writerow(headers)
#
#     for uberX_request, data in uberX_requests.iteritems():
#             writer.writerow([data.get("eta").requested_time, uberX_request, data.get("surge_rate").surge, data.get("eta").estimate])
#
#
# '''
# Get bus data
# '''
#
# all_bus = []
#
# with open("/Users/lorenamesa/Desktop/pytennessee/bus_data.csv", "r") as csvdata:
#     headers = ['distance_to_stop', 'rt', 'vehicle_id', 'prdtm', 'tmstmp', 'rtdir', 'stpnm']
#     reader = csv.reader(csvdata)
#
#     for row in reader:
#         data = dict(zip(headers, row))
#         bus_prediction = BusPrediction(**data)
#         local_datetime = datetime.strptime(bus_prediction.arrival_time, "%Y%m%d %H:%M").replace(tzinfo=tz.tzlocal())
#         bus_prediction.requested_time = int((local_datetime - datetime(1970, 1, 1, tzinfo=tz.tzutc())).total_seconds())
#         all_bus.append(bus_prediction)
#
#
#     north_ave_etas = [bus_eta for bus_eta in all_bus if 6 < bus_eta.get_requested_time_hr() < 12 and bus_eta.stop_name == 'North Ave & California']
#     cali_st_etas = [bus_eta for bus_eta in all_bus if 6 < bus_eta.get_requested_time_hr() < 12 and bus_eta.stop_name == 'California & Le Moyne']
#
#     print len(north_ave_etas)  # 461
#     print len(cali_st_etas)  # 469
#
# with open("/Users/lorenamesa/Desktop/pytennessee/bus_non-labeled_data.csv", "w") as csvdata:
#     headers = ['requested_time', 'route', 'direction', 'stop_name', 'eta', 'delayed']
#
#     writer = csv.writer(csvdata, dialect='excel')
#     writer.writerow(headers)
#
#     for bus_prediction in north_ave_etas:
#             writer.writerow([bus_prediction.requested_time, bus_prediction.route,
#                              bus_prediction.route_direction, bus_prediction.stop_name,
#                              bus_prediction.bus_eta, "0"])
#
#     for bus_prediction in cali_st_etas:
#             writer.writerow([bus_prediction.requested_time, bus_prediction.route,
#                              bus_prediction.route_direction, bus_prediction.stop_name,
#                              bus_prediction.bus_eta, "0"])
#
#
# '''
# Get train data
# '''
# all_train = []
#
# with open("/Users/lorenamesa/Desktop/pytennessee/train_data.csv", "r") as csvdata:
#     headers = ['isDly','rt','isFlt','arrT','prdt','is_scheduled','staNm','is_approached','trDr']
#     reader = csv.reader(csvdata)
#
#     for row in reader:
#         data = dict(zip(headers, row))
#         train_p = TrainPrediction(**data)
#         all_train.append(train_p)
#
#         local_datetime = datetime.strptime(train_p.arrival_time, "%Y%m%d %H:%M:%S").replace(tzinfo=tz.tzlocal())
#         train_p.requested_time = int((local_datetime - datetime(1970, 1, 1, tzinfo=tz.tzutc())).total_seconds())
#
#     north_ave_etas = [train_eta for train_eta in all_train if 6 < train_eta.get_requested_time_hr() < 12 and train_eta.stop_name == 'Damen']
#
#     cali_st_etas = [train_eta for train_eta in all_train if 6 < train_eta.get_requested_time_hr() < 12 and train_eta.stop_name == 'California']
#
#     print len(cali_st_etas)  # 718
#     print len(north_ave_etas) # 589
#
# with open("/Users/lorenamesa/Desktop/pytennessee/train_non-labeled_data.csv", "w") as csvdata:
#     headers = ['requested_time', 'route', 'direction', 'stop_name', 'eta', 'delayed']
#
#     writer = csv.writer(csvdata, dialect='excel')
#     writer.writerow(headers)
#     count = 0
#     for train_p in north_ave_etas:
#             writer.writerow([train_p.requested_time, train_p.route, train_p.train_direction,
#                              train_p.stop_name, train_p.train_eta, train_p.is_delayed])
#
#
#     for train_p in cali_st_etas:
#             writer.writerow([train_p.requested_time, train_p.route, train_p.train_direction,
#                              train_p.stop_name, train_p.train_eta, train_p.is_delayed])
#
# '''
# Compile the flattened features below.
# '''
#
# with open("/Users/lorenamesa/Desktop/pytennessee/train_non-labeled_data.csv", "r") as traindata:
#     headers = ['requested_time', 'route', 'direction', 'stop_name', 'eta', 'delayed']
#     reader = csv.reader(traindata)
#
#     for row in reader:
#         train = dict(zip(headers, row))
#         train['type'] = 'train'
#         if dates.get(row[0]):
#             dates[row[0]].append(train)
#         else:
#             dates[row[0]] = [train]
#
#
# with open("/Users/lorenamesa/Desktop/pytennessee/bus_non-labeled_data.csv", "r") as busdata:
#     headers = ['requested_time', 'route', 'direction', 'stop_name', 'eta', 'delayed']
#
#     reader = csv.reader(busdata)
#     for row in reader:
#         bus = dict(zip(headers, row))
#         bus['type'] = 'bus'
#         if dates.get(row[0]):
#             dates[row[0]].append(bus)
#         else:
#             dates[row[0]] = [bus]
#
# with open("/Users/lorenamesa/Desktop/pytennessee/weather_labeled_data.csv", "r") as weatherdata:
#     headers = ['date', 'weather', 'feels_like']
#
#     reader = csv.reader(weatherdata)
#     for row in reader:
#         weather = dict(zip(headers, row))
#         weather['type'] = 'weather'
#         if dates.get(row[0]):
#             dates[row[0]].append(weather)
#         else:
#             dates[row[0]] = [weather]
#
# with open("/Users/lorenamesa/Desktop/pytennessee/uberx_morning_data_nonlabeled.csv", "r") as uberxdata:
#     headers = ['request_time', 'request_id', 'surge_rate', 'eta']
#
#     reader = csv.reader(uberxdata)
#     for row in reader:
#         uberX = dict(zip(headers, row))
#         uberX['type'] = 'uberX'
#
#         if dates.get(row[0]):
#             dates[row[0]].append(uberX)
#         else:
#             dates[row[0]] = [uberX]
#
# with open("/Users/lorenamesa/Desktop/pytennessee/tweet_labeled_data.csv", "r") as tweetdata:
#     headers = ['created_at', 'tweet_id', 'text']
#
#     reader = csv.reader(tweetdata)
#     for row in reader:
#         tweet = dict(zip(headers, row))
#         tweet['type'] = 'tweet'
#         if dates.get(row[0]):
#             dates[row[0]].append(tweet)
#         else:
#             dates[row[0]] = [tweet]
#
# with open("/Users/lorenamesa/Desktop/pytennessee/final_morning_data.csv", "w") as alldata:
#     headers = ['type', 'created_at', 'date_string', 'data']
#
#     writer = csv.writer(alldata, dialect='excel')
#     writer.writerow(headers)
#
#     for type, data in dates.iteritems():
#         for d in data:
#             date = d.get('created_at') or d.get('requested_time') or d.get('date') or d.get('request_time')
#             if date is not None and date != 'date' and date != 'requested_time' and date != 'created_at' and date != 'request_time':
#                 time_date = datetime.fromtimestamp(float(date)).replace(tzinfo=tz.tzlocal())
#                 time_date = time_date.strftime('%Y-%m-%d %H:%M')
#                 writer.writerow([d.get('type'), date, time_date, d])



# all_data = []
#
# with open("/Users/lorenamesa/Desktop/pytennessee/final_morning_data_sorted.csv", "r") as alldata:
#     headers = ['type', 'created_at', 'date_string', 'data']
#
#     writer = csv.reader(alldata, dialect='excel')
#
#     for row in writer:
#         if row[0] == 'type':
#             continue
#         try:
#             data = json.loads(row[3].replace("'", '"'))
#             type = data.get('type')
#             if type == "train" and data.get("stop_name"):
#                 type = data.get("stop_name") + "_" + "train"
#             elif type == "bus" and data.get("route"):
#                 type = data.get("route") + "_" + "bus"
#             row[0] = type
#             all_data.append(row)
#         except Exception:
#             continue

'''
Step 2: Take sorted data, strip out data needed for each feature.
'''

# all_data = []
#
# with open("/Users/lorenamesa/Desktop/pytennessee/final_morning_data_sorted.csv", "r") as alldata:
#     headers = ['type', 'created_at', 'date_string', 'data']
#
#     reader = csv.reader(alldata, dialect='excel')
#
#     for row in reader:
#         try:
#             data = json.loads(row[3].replace("'", '"'))
#             type = data.get('type')
#             if type == "train" and data.get("stop_name"):
#                 type = data.get("stop_name") + "_" + "train"
#             elif type == "bus" and data.get("route"):
#                 type = data.get("route") + "_" + "bus"
#             row[0] = type
#             all_data.append(row)
#         except Exception:
#             continue
#
# features = ["California_train", "weather", "feels_like", "tweet", "Damen_train", "uber_surging", "uber_eta", "72_bus", "52_bus"]
# expanded_features = []
#
# for item in all_data:
#     data = json.loads(item[3].replace("'", '"'))
#
#     if item[0] == 'uberX':
#         uber_1 = ['uber_surging', item[1], item[2], data['surge_rate']]
#         uber_2 = ['uber_eta', item[1], item[2], data['eta']]
#         expanded_features.append(uber_1)
#         expanded_features.append(uber_2)
#         continue
#     if item[0] == 'Damen_train':
#         eta = data['eta']
#         expanded_features.append(['Damen_train', item[1], item[2], eta])
#         continue
#     if item[0] == 'California_train':
#         expanded_features.append(['California_train', item[1], item[2], data['eta']])
#         continue
#     if item[0] == '72_bus':
#         expanded_features.append(['72_bus', item[1], item[2], data['eta']])
#         continue
#     if item[0] == '52_bus':
#         expanded_features.append(['52_bus', item[1], item[2], data['eta']])
#         continue
#     if item[0] == 'tweet':
#         expanded_features.append(['tweet', item[1], item[2], data['text']])
#         continue
#     if item[0] == 'weather':
#         weather_one = ['weather', item[1], item[2], data['weather']]
#         weather_two = ['feels_like', item[1], item[2], data['feels_like']]
#         expanded_features.append(weather_one)
#         expanded_features.append(weather_two)
#
# with open("/Users/lorenamesa/Desktop/pytennessee/final_morning_data_features.csv", "w") as alldata:
#     headers = ['feature', 'created_at', 'date_string', 'data']
#
#     writer = csv.writer(alldata, dialect='excel')
#     writer.writerow(headers)
#
#     for d in expanded_features:
#         writer.writerow(d)

'''
Step 3: Take feature data and change continuous data into categorical data with some analysis with
pylab, zip into single entities to produce training data.
'''
#
features = {}

with open("/Users/lorenamesa/Desktop/pytennessee/final_morning_data_features.csv", "r") as alldata:
    headers = ['feature', 'created_at', 'date_string', 'data']

    reader = csv.reader(alldata, dialect='excel')

    for row in reader:
        if row[0] not in features:
            features[row[0]] = [row]
        else:
            features[row[0]].append(row)

for type, data in features.iteritems():
    print type, len(data)

'''
Raw morning data:
72_bus 308
uber_eta 117
tweet 5
feature 1
uber_surging 117
California_train 718
weather 182
52_bus 329
Damen_train 589
feels_like 182
'''

headers = ["utc_timestamp", "date_string", "prediction", "california_train", "weather", "feels_like", "tweet", "damen_train", "uber_surging", "uber_eta", "72_bus", "52_bus"]
headers_to_indx = dict(zip(headers, [num for num in xrange(11)]))


# {'72_bus': 9, 'uber_eta': 8, 'tweet': 5, 'California_train': 2, 'utc_timestamp': 0, 'Damen_train': 6, 'weather': 3, '52_bus': 10, 'uber_surging': 7, 'feels_like': 4, 'date_string': 1}

print headers_to_indx

flattened_features = []
for item in features['weather']:
    string_time = item[2]
    utctimestamp = int(item[1])
    utc_for_quart_hour = [901]
    utc_for_full_hr = [utctimestamp, utctimestamp + 901, utctimestamp + (901*2), utctimestamp + (901*3)]
    hour = datetime.fromtimestamp(utctimestamp).replace(tzinfo=tz.tzlocal()).hour
    if 6 < hour < 12:
        for time in utc_for_full_hr:
            string_time = datetime.fromtimestamp(float(time)).replace(tzinfo=tz.tzlocal())
            string_time = string_time.strftime('%Y-%m-%d %H:%M')
            final_feature = [time, string_time, None, item[3], None, None, None, None, None, None, None]
            for feature, data in features.iteritems():
                if feature != "weather" and feature != "feature":
                    if not final_feature[headers_to_indx[feature]]:
                        indx = None
                        diffs = []
                        for d in data:
                            # print d
                            diffs.append(abs(int(d[1]) - time))
                        smallest_diff = min(diffs)
                        indx = diffs.index(smallest_diff)
                        print smallest_diff, indx
                        if feature == "tweet" and smallest_diff > 15077:
                            final_feature[headers_to_indx[feature]] = 0
                        elif feature == "tweet":
                            final_feature[headers_to_indx[feature]] = 1
                        else:
                            final_feature[headers_to_indx[feature]] = data[indx][3]
            flattened_features.append(final_feature)

'''
Transform continuous features into categorical features.
'''

# Flatten uberX_surging data
uberX_surging = [float(feature[8]) for feature in flattened_features]
pylab.figure()
uberX_surging_data = pylab.hist(uberX_surging, bins=6)

# pylab.title("Range of UberX Surging Rates in January 2016 From Home to Work Between 6am to 12pm")
# pylab.legend(loc='best')
# pylab.xlabel("Surging Rate")
# pylab.ylabel("Number of UberXs")
# pylab.plot()
# pylab.show()

ranges = list(uberX_surging_data[1][0:7])
categories = []
num_categories = []

for num in xrange(len(ranges)-1):
    categories.append(str(ranges[num]) + " to " + str(ranges[num+1]))

for num in xrange(len(ranges)-1):
    num_categories.append([ranges[num],ranges[num+1]])

print 'uberx surge categories: ', categories  #

changed_uberX_surging = []
for uberX in uberX_surging:
    for category in num_categories:
        if category[0] <= float(uberX) < category[1]:
            changed_uberX_surging.append(str(category[0]) + " to " + str(category[1]))
            break
        elif category[0] < float(uberX) <= category[1]:
            changed_uberX_surging.append(str(category[0]) + " to " + str(category[1]))
            break

for indx, feature in enumerate(flattened_features):
    feature[8] = changed_uberX_surging[indx]

# Flatten uberX_eta data

uberX_etas = [float(feature[9]) for feature in flattened_features]

pylab.figure()
uberx_eta_data = pylab.hist(uberX_etas, bins=6)

# pylab.title("Range of Uber ETAs in January 2016 From Home to Work Between 6am to 12pm")
# pylab.legend(loc='best')
# pylab.xlabel("Minutes Until Pickup")
# pylab.ylabel("Number of Ubers")
# pylab.plot()
# pylab.show()

ranges = list(uberx_eta_data[1][0:7])
categories = []
num_categories = []

for num in xrange(len(ranges)-1):
    categories.append(str(ranges[num]) + " to " + str(ranges[num+1]))

for num in xrange(len(ranges)-1):
    num_categories.append([ranges[num], ranges[num+1]])

print 'uberx eta categories: ', categories  #

changed_uberX_eta = []
for uberX_eta in uberX_etas:
    for category in num_categories:
        if category[0] <= uberX_eta < category[1]:
            changed_uberX_eta.append(str(category[0]) + " to " + str(category[1]))
            break
        elif category[0] < float(uberX_eta) <= category[1]:
            changed_uberX_eta.append(str(category[0]) + " to " + str(category[1]))
            break

for indx, feature in enumerate(flattened_features):
    feature[9] = changed_uberX_eta[indx]


# North Ave Bus

north_ave_etas = [float(feature[10]) for feature in flattened_features]

pylab.figure()
data = pylab.hist(north_ave_etas, bins=6)

# pylab.title("Range of North Ave Bus ETAs in January 2016 From Home to Work Between 6am to 12pm")
# pylab.legend(loc='best')
# pylab.xlabel("Minutes Until Pickup")
# pylab.ylabel("Number of Buses")
# pylab.plot()
# pylab.show()

ranges = list(data[1][0:7])
categories = []  # ['0.0 to 5.16666666667', '5.16666666667 to 10.3333333333', '10.3333333333 to 15.5', '15.5 to 20.6666666667', '20.6666666667 to 25.8333333333', '25.8333333333 to 31.0']
num_categories = []

for num in xrange(len(ranges)-1):
    categories.append(str(ranges[num]) + " to " + str(ranges[num+1]))

for num in xrange(len(ranges)-1):
    num_categories.append([ranges[num], ranges[num+1]])

print 'north bus categories: ', categories  #

changed_north_bus = []
for bus_prediction in north_ave_etas:
    for category in num_categories:
        if category[0] <= float(bus_prediction) < category[1]:
            changed_north_bus.append(str(category[0]) + " to " + str(category[1]))
            break
        elif category[0] < float(bus_prediction) <= category[1]:
            changed_north_bus.append(str(category[0]) + " to " + str(category[1]))
            break

for indx, feature in enumerate(flattened_features):
    feature[10] = changed_north_bus[indx]

# Cali Bus

cali_st_etas = [float(feature[11]) for feature in flattened_features]

print len(cali_st_etas)  # 469
pylab.figure()
cali_data = pylab.hist(cali_st_etas, bins=6)
#
# pylab.title("Range of California Bus ETAs in January 2016 From Home to Work Between 6am to 12pm")
# pylab.legend(loc='best')
# pylab.xlabel("Minutes Until Pickup")
# pylab.ylabel("Number of Buses")
# pylab.plot()
# pylab.show()

cali_ranges = list(cali_data[1][0:7])
cali_categories = []  # ['0.0 to 5.16666666667', '5.16666666667 to 10.3333333333', '10.3333333333 to 15.5', '15.5 to 20.6666666667', '20.6666666667 to 25.8333333333', '25.8333333333 to 31.0']
cali_num_categories = []

for num in xrange(len(cali_ranges)-1):
    cali_categories.append(str(cali_ranges[num]) + " to " + str(cali_ranges[num+1]))

for num in xrange(len(cali_ranges)-1):
    cali_num_categories.append([cali_ranges[num], cali_ranges[num+1]])

print 'cali bus categories: ', categories  #

changed_cali_bus = []
for bus_prediction in cali_st_etas:
    for category in cali_num_categories:
        if category[0] <= float(bus_prediction) < category[1]:
            changed_cali_bus.append(str(category[0]) + " to " + str(category[1]))
            break
        elif category[0] < float(bus_prediction) <= category[1]:
            changed_cali_bus.append(str(category[0]) + " to " + str(category[1]))
            break

for indx, feature in enumerate(flattened_features):
    feature[11] = changed_cali_bus[indx]

# Damen Blue line Train

damen_etas = [float(feature[7]) for feature in flattened_features]
pylab.figure()
damen_t_data = pylab.hist(damen_etas, bins=6)

# pylab.title("Range of Damen Blue Line Train ETAs in January 2016 From Home to Work Between 6am to 12pm")
# pylab.legend(loc='best')
# pylab.xlabel("Minutes Until Arrival")
# pylab.ylabel("Number of Trains")
# pylab.plot()
# pylab.show()

ranges = list(damen_t_data[1][0:7])
categories = []  # ['1.0 to 5.5', '5.5 to 10.0', '10.0 to 14.5', '14.5 to 19.0', '19.0 to 23.5', '23.5 to 28.0']
num_categories = []

for num in xrange(len(ranges)-1):
    categories.append(str(ranges[num]) + " to " + str(ranges[num+1]))

for num in xrange(len(ranges)-1):
    num_categories.append([ranges[num], ranges[num+1]])

print 'damen train categories: ', categories  #

changed_damen_t = []
for train_p in damen_etas:
    for category in num_categories:
        if category[0] <= float(train_p) < category[1]:
            changed_damen_t.append(str(category[0]) + " to " + str(category[1]))
            break
        elif category[0] < float(train_p) <= category[1]:
            changed_damen_t.append(str(category[0]) + " to " + str(category[1]))
            break

for indx, feature in enumerate(flattened_features):
    feature[7] = changed_damen_t[indx]

# California Blue Line Train
cali_etas = [float(feature[2]) for feature in flattened_features]
pylab.figure()
cali_t_data = pylab.hist(cali_etas, bins=6)
#
# pylab.title("Range of California Blue Line Train ETAs in January 2016 From Home to Work Between 6am to 12pm")
# pylab.legend(loc='best')
# pylab.xlabel("Minutes Until Arrival")
# pylab.ylabel("Number of Trains")
# pylab.plot()
# pylab.show()

ranges = list(cali_t_data[1][0:7])
categories = []  # ['1.0 to 4.5', '4.5 to 8.0', '8.0 to 11.5', '11.5 to 15.0', '15.0 to 18.5', '18.5 to 22.0']
num_categories = []

for num in xrange(len(ranges)-1):
    categories.append(str(ranges[num]) + " to " + str(ranges[num+1]))

for num in xrange(len(ranges)-1):
    num_categories.append([ranges[num], ranges[num+1]])
# print num_categories
print 'cali train categories: ', categories  #

changed_cali_t = []
for train_p in cali_etas:
    for category in num_categories:
        if category[0] <= float(train_p) < category[1]:
            changed_cali_t.append(str(category[0]) + " to " + str(category[1]))
            break
        elif category[0] < float(train_p) <= category[1]:
            changed_cali_t.append(str(category[0]) + " to " + str(category[1]))
            break
print cali_etas

for indx, feature in enumerate(flattened_features):
    feature[2] = changed_cali_t[indx]


'''
uberx surge categories:  ['1.0 to 1.15', '1.15 to 1.3', '1.3 to 1.45', '1.45 to 1.6', '1.6 to 1.75', '1.75 to 1.9']
uberx eta categories:  ['2.0 to 3.5', '3.5 to 5.0', '5.0 to 6.5', '6.5 to 8.0', '8.0 to 9.5', '9.5 to 11.0']
north bus categories:  ['1.0 to 6.0', '6.0 to 11.0', '11.0 to 16.0', '16.0 to 21.0', '21.0 to 26.0', '26.0 to 31.0']
cali bus categories:  ['1.0 to 6.0', '6.0 to 11.0', '11.0 to 16.0', '16.0 to 21.0', '21.0 to 26.0', '26.0 to 31.0']
damen train categories:  ['1.0 to 5.16666666667', '5.16666666667 to 9.33333333333', '9.33333333333 to 13.5', '13.5 to 17.6666666667', '17.6666666667 to 21.8333333333', '21.8333333333 to 26.0']
cali train categories:  ['1.0 to 4.0', '4.0 to 7.0', '7.0 to 10.0', '10.0 to 13.0', '13.0 to 16.0', '16.0 to 19.0']
'''

with open("/Users/lorenamesa/Desktop/pytennessee/final_morning_training_data.csv", "w") as morning_data:

    writer = csv.writer(morning_data, dialect='excel')
    writer.writerow(headers)

    for row in flattened_features:
        writer.writerow(row)





