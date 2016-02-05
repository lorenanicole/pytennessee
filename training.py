import csv
import json
from dateutil import tz
from datetime import datetime

dates = {}
all_data = {}

with open("/Users/lorenamesa/Desktop/pytennessee/train_labeled_data.csv", "r") as traindata:
    headers = ['requested_time', 'route', 'direction', 'stop_name', 'eta', 'delayed']
    reader = csv.reader(traindata)

    for row in reader:
        train = dict(zip(headers, row))
        train['type'] = 'train'
        if dates.get(row[0]):
            dates[row[0]].append(train)
        else:
            dates[row[0]] = [train]


with open("/Users/lorenamesa/Desktop/pytennessee/bus_labeled_data.csv", "r") as busdata:
    headers = ['requested_time', 'route', 'direction', 'stop_name', 'eta', 'delayed']

    reader = csv.reader(busdata)
    for row in reader:
        bus = dict(zip(headers, row))
        bus['type'] = 'bus'
        if dates.get(row[0]):
            dates[row[0]].append(bus)
        else:
            dates[row[0]] = [bus]

with open("/Users/lorenamesa/Desktop/pytennessee/weather_labeled_data.csv", "r") as weatherdata:
    headers = ['date', 'weather', 'feels_like']

    reader = csv.reader(weatherdata)
    for row in reader:
        weather = dict(zip(headers, row))
        weather['type'] = 'weather'
        if dates.get(row[0]):
            dates[row[0]].append(weather)
        else:
            dates[row[0]] = [weather]

with open("/Users/lorenamesa/Desktop/pytennessee/uberx_morning_labeled_data.csv", "r") as uberxdata:
    headers = ['request_time', 'request_id', 'surge_rate', 'eta']

    reader = csv.reader(uberxdata)
    for row in reader:
        uberX = dict(zip(headers, row))
        uberX['type'] = 'uberX'

        if dates.get(row[0]):
            dates[row[0]].append(uberX)
        else:
            dates[row[0]] = [uberX]

with open("/Users/lorenamesa/Desktop/pytennessee/tweet_labeled_data.csv", "r") as tweetdata:
    headers = ['created_at', 'tweet_id', 'text']

    reader = csv.reader(tweetdata)
    for row in reader:
        tweet = dict(zip(headers, row))
        tweet['type'] = 'tweet'
        # print tweet.get('created_at')
        if dates.get(row[0]):
            dates[row[0]].append(tweet)
        else:
            dates[row[0]] = [tweet]

with open("/Users/lorenamesa/Desktop/pytennessee/all_morning_labeled_data.csv", "w") as alldata:
    headers = ['type', 'created_at', 'date_string', 'data']

    writer = csv.writer(alldata, dialect='excel')
    writer.writerow(headers)

    for type, data in dates.iteritems():
        for d in data:
            date = d.get('created_at') or d.get('requested_time') or d.get('date') or d.get('request_time')
            if date is not None and date != 'date' and date != 'requested_time' and date != 'created_at' and date != 'request_time':
                # print date
                time_date = datetime.fromtimestamp(float(date)).replace(tzinfo=tz.tzlocal())
                time_date = time_date.strftime('%Y-%m-%d %H:%M')
                writer.writerow([d.get('type'), date, time_date, d])



all_data = []

with open("/Users/lorenamesa/Desktop/pytennessee/all_morning_data_sorted.csv", "r") as alldata:
    headers = ['type', 'created_at', 'date_string', 'data']

    writer = csv.reader(alldata, dialect='excel')

    for row in writer:
        if row[0] == 'type':
            continue
        try:
            data = json.loads(row[3].replace("'", '"'))
            type = data.get('type')
            if type == "train" and data.get("stop_name"):
                type = data.get("stop_name") + "_" + "train"
            elif type == "bus" and data.get("route"):
                type = data.get("route") + "_" + "bus"
            row[0] = type
            all_data.append(row)
        except Exception:
            continue

# with open("/Users/lorenamesa/Desktop/pytennessee/all_morning_data_sorted_2.csv", "w") as alldata:
#     headers = ['type', 'created_at', 'date_string', 'data']
#
#     writer = csv.writer(alldata, dialect='excel')
#     writer.writerow(headers)
#
#     for d in all_data:
#         writer.writerow(d)

features = ["California_train", "weather", "feels_like", "tweet", "Damen_train", "uber_surging", "uber_eta", "72_bus", "52_bus"]
expanded_features = []

for item in all_data:
    data = json.loads(item[3].replace("'", '"'))

    if item[0] == 'uberX':
        uber_1 = ['uber_surging', item[1], item[2], data['surge_rate']]
        uber_2 = ['uber_eta', item[1], item[2], data['eta']]
        expanded_features.append(uber_1)
        expanded_features.append(uber_2)
        continue
    if item[0] == 'Damen_train':
        eta = data['eta']
        expanded_features.append(['Damen_train', item[1], item[2], eta])
        continue
    if item[0] == 'California_train':
        expanded_features.append(['California_train', item[1], item[2], data['eta']])
        continue
    if item[0] == '72_bus':
        expanded_features.append(['72_bus', item[1], item[2], data['eta']])
        continue
    if item[0] == '52_bus':
        expanded_features.append(['52_bus', item[1], item[2], data['eta']])
        continue
    if item[0] == 'tweet':
        expanded_features.append(['tweet', item[1], item[2], data['text']])
        continue
    if item[0] == 'weather':
        weather_one = ['weather', item[1], item[2], data['weather']]
        weather_two = ['feels_like', item[1], item[2], data['feels_like']]
        expanded_features.append(weather_one)
        expanded_features.append(weather_two)

with open("/Users/lorenamesa/Desktop/pytennessee/all_morning_data_features.csv", "w") as alldata:
    headers = ['feature', 'created_at', 'date_string', 'data']

    writer = csv.writer(alldata, dialect='excel')
    writer.writerow(headers)

    for d in expanded_features:
        # if d[0] == "Damen_train":
        #     if d[3] == "1.0":
        #         d[3] = "1.0 to 5.5"
        #     if d[3] == "19.0":
        #         d[3] = "19.0 to 23.5"
        #     if d[3] == "10.0":
        #         d[3] = "10.0 to 14.5"
        #     if d[3] == "15.0":
        #         d[3] = "14.5 to 19.0"
        #     if d[3] == "8.0":
        #         d[3] = "5.5 to 10.0"
        # if d[0] == "California_train":
        #     if d[3] == "1.0":
        #         d[3] = "1.0 to 5.5"
        #     if d[3] == "19.0":
        #         d[3] = "19.0 to 23.5"
        #     if d[3] == "10.0":
        #         d[3] = "10.0 to 14.5"
        #     if d[3] == "15.0":
        #         d[3] = "14.5 to 19.0"
        #     if d[3] == "8.0":
        #         d[3] = "5.5 to 10.0"
        # if d[0] == "uber_eta":
        #     if d[3] == "5.0":
        #         d[3] = "5.0 to 6.5"
        #     if d[3] == "2.0":
        #         d[3] = "2.0 to 3.5"
        #     if d[3] == "11.0":
        #         d[3] = "9.5 to 11.0"
        writer.writerow(d)

features = {}

with open("/Users/lorenamesa/Desktop/pytennessee/all_morning_data_features.csv", "r") as alldata:
    headers = ['feature', 'created_at', 'date_string', 'data']

    reader = csv.reader(alldata, dialect='excel')

    for row in reader:
        if row[0] not in features:
            features[row[0]] = [row]
        else:
            features[row[0]].append(row)

# 72_bus 308
# uber_eta 117
# tweet 5
# feature 1
# uber_surging 117
# California_train 718
# weather 182
# 52_bus 329
# Damen_train 589
# feels_like 182


headers = ["utc_timestamp", "date_string", "California_train", "weather", "feels_like", "tweet", "Damen_train", "uber_surging", "uber_eta", "72_bus", "52_bus"]
headers_to_indx = dict(zip(headers, [num for num in xrange(11)]))


# {'72_bus': 9, 'uber_eta': 8, 'tweet': 5, 'California_train': 2, 'utc_timestamp': 0, 'Damen_train': 6, 'weather': 3, '52_bus': 10, 'uber_surging': 7, 'feels_like': 4, 'date_string': 1}

print headers_to_indx

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

with open("/Users/lorenamesa/Desktop/pytennessee/morning_training_data.csv", "w") as morning_data:

    writer = csv.writer(morning_data, dialect='excel')
    writer.writerow(headers)

    for row in flattened_features:
        writer.writerow(row)
#





