import csv
import pylab
import json
import re
import csv
import numpy as np

from random import shuffle

from sklearn import metrics
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB

headers = ["utc_timestamp", "date_string", "prediction", "california_train", "weather", "feels_like", "tweet", "damen_train", "uber_surging", "uber_eta", "72_bus", "52_bus"]
headers_to_indx = dict(zip(headers, [num for num in xrange(11)]))


# {'72_bus': 9, 'uber_eta': 8, 'tweet': 5, 'California_train': 2, 'utc_timestamp': 0, 'Damen_train': 6, 'weather': 3, '52_bus': 10, 'uber_surging': 7, 'feels_like': 4, 'date_string': 1}

class WorkCommutePrediction(object):

    def __init__(self, **kwargs):
        self.labeled_route = kwargs.get('prediction')
        self.utc_timestamp = kwargs.get('utc_timestamp')
        self.local_date_string = kwargs.get('date_string')
        self.weather = kwargs.get('weather')
        self.feels_like = kwargs.get('feels_like')
        self.cta_delayed = kwargs.get('tweet')
        self.north_ave_bus_eta = kwargs.get('72_bus')
        self.cali_bus_eta = kwargs.get('52_bus')
        self.damen_train_eta = kwargs.get('damen_train')
        self.cali_train_eta = kwargs.get('california_train')
        self.uberX_eta = kwargs.get('uber_eta')
        self.uberX_surging = kwargs.get('uber_surging')

all_routes = {}
raw_routes_data = []
all_labels = []
with open("/Users/lorenamesa/Desktop/pytennessee/final_morning_training_data.csv", "r") as morning_data:

    reader = csv.reader(morning_data, dialect='excel')

    for row in reader:
        if row[0] == 'utc_timestamp':
            continue
        data = dict(zip(headers, row))
        all_labels.append(data.pop('prediction'))
        raw_route_data = dict(zip(headers, row))
        raw_route_data.pop('prediction')
        raw_route_data.pop('date_string')
        raw_route_data.pop('utc_timestamp')
        raw_routes_data.append(raw_route_data)
        work_commute_p = WorkCommutePrediction(**data)
        if all_routes.get(work_commute_p.labeled_route):
            all_routes[work_commute_p.labeled_route].append(work_commute_p)
        else:
            all_routes[work_commute_p.labeled_route] = [work_commute_p]

route_data = []
routes = []

# route_num_to_name = {"1": "52 Bus -> California Train", "2": "72 Bus -> Damen Train", "3": "UberX"}
#
# for route, data in all_routes.iteritems():
#     routes.append(route_num_to_name[route])
#     route_data.append(len(data))

# pylab.figure()
# pylab.title('Training Data by Routes')
# pylab.pie(route_data, labels=routes, autopct='%1.1f%%', shadow=True, startangle=90)
# pylab.show()

# weather_breakdown = {}
# for route, data in all_routes.iteritems():
#     weather_breakdown[route] = {}
#     for item in data:
#         if weather_breakdown[route].get(item.feels_like):
#             weather_breakdown[route][item.feels_like] += 1
#         else:
#             weather_breakdown[route][item.feels_like] = 1
#
# print weather_breakdown

# feels_like = ['18.0 to 22.8333333333','22.8333333333 to 27.6666666667','27.6666666667 to 32.5','32.5 to 37.3333333333','37.3333333333 to 42.1666666667','42.1666666667 to 47.0']
# shortened = ['18.0-22.83','22.83-27.66','27.66-32.5','32.5-37.33','37.33-42.16','42.16-47.0']

#
# pylab.figure()
# pylab.title('Number of Rides Per Route By Weather')
# b1 = pylab.bar([1,2,3,4,5,6], [weather_breakdown['1'].get(item,0) for item in feels_like], color='red', width=0.3)
# b2 = pylab.bar([1,2,3,4,5,6], [weather_breakdown['2'].get(item,0) for item in feels_like], color='orange', width=0.2)
# b3 = pylab.bar([1,2,3,4,5,6], [weather_breakdown['3'].get(item,0) for item in feels_like], color='blue', width=0.1)
#
# pylab.legend([b1[0], b2[0], b3[0]], ['52 Bus -> Cali Train', '72 Bus -> Damen', 'UberX'])
# pylab.xticks([1,2,3,4,5,6], shortened)
#
#
# pylab.xlabel('Weather')
# pylab.ylabel('Number of Commutes')
# pylab.show()
#
# north_bus_breakdown = {}
# for route, data in all_routes.iteritems():
#     north_bus_breakdown[route] = {}
#     for item in data:
#         if north_bus_breakdown[route].get(item.north_ave_bus_eta):
#             north_bus_breakdown[route][item.north_ave_bus_eta] += 1
#         else:
#             north_bus_breakdown[route][item.north_ave_bus_eta] = 1
#
# print north_bus_breakdown
#
# north_eta = ['1.0 to 6.0', '6.0 to 11.0', '11.0 to 16.0', '16.0 to 21.0', '21.0 to 26.0', '26.0 to 31.0']
#
# pylab.figure()
# pylab.title('Number of Rides Per Route By North Ave (#72) Bus ETA')
# b1 = pylab.bar([1,2,3,4,5,6], [north_bus_breakdown['1'].get(item,0) for item in north_eta], color='red', width=0.3)
# b2 = pylab.bar([1,2,3,4,5,6], [north_bus_breakdown['2'].get(item,0) for item in north_eta], color='orange', width=0.2)
# b3 = pylab.bar([1,2,3,4,5,6], [north_bus_breakdown['3'].get(item,0) for item in north_eta], color='blue', width=0.1)
#
# pylab.legend([b1[0], b2[0], b3[0]], ['52 Bus -> Cali Train', '72 Bus -> Damen', 'UberX'])
# pylab.xticks([1,2,3,4,5,6], north_eta)
#
#
# pylab.xlabel('North Ave Bus ETA in Minutes')
# pylab.ylabel('Number of Commutes')
# pylab.show()


# cali_bus_breakdown = {}
# for route, data in all_routes.iteritems():
#     cali_bus_breakdown[route] = {}
#     for item in data:
#         if cali_bus_breakdown[route].get(item.cali_bus_eta):
#             cali_bus_breakdown[route][item.cali_bus_eta] += 1
#         else:
#             cali_bus_breakdown[route][item.cali_bus_eta] = 1
#
# print cali_bus_breakdown
#
# cali_eta = ['1.0 to 6.0', '6.0 to 11.0', '11.0 to 16.0', '16.0 to 21.0', '21.0 to 26.0', '26.0 to 31.0']
#
# pylab.figure()
# pylab.title('Number of Rides Per Route By California Ave (#52) Bus ETA')
# b1 = pylab.bar([1,2,3,4,5,6], [cali_bus_breakdown['1'].get(item,0) for item in cali_eta], color='red', width=0.3)
# b2 = pylab.bar([1,2,3,4,5,6], [cali_bus_breakdown['2'].get(item,0) for item in cali_eta], color='orange', width=0.2)
# b3 = pylab.bar([1,2,3,4,5,6], [cali_bus_breakdown['3'].get(item,0) for item in cali_eta], color='blue', width=0.1)
#
# pylab.legend([b1[0], b2[0], b3[0]], ['52 Bus -> Cali Train', '72 Bus -> Damen', 'UberX'])
# pylab.xticks([1,2,3,4,5,6], cali_eta)
#
#
# pylab.xlabel('California (#52) Bus ETA in Minutes')
# pylab.ylabel('Number of Commutes')
# pylab.show()

# uber_breakdown = {}
# for route, data in all_routes.iteritems():
#     uber_breakdown[route] = {}
#     for item in data:
#         if uber_breakdown[route].get(item.uberX_eta):
#             uber_breakdown[route][item.uberX_eta] += 1
#         else:
#             uber_breakdown[route][item.uberX_eta] = 1
#
# print uber_breakdown
#
# uber_eta = ['2.0 to 3.5', '3.5 to 5.0', '5.0 to 6.5', '6.5 to 8.0', '8.0 to 9.5', '9.5 to 11.0']
#
# pylab.figure()
# pylab.title('Number of Rides Per Route By UberX ETA')
# b1 = pylab.bar([1,2,3,4,5,6], [uber_breakdown['1'].get(item,0) for item in uber_eta], color='red', width=0.3)
# b2 = pylab.bar([1,2,3,4,5,6], [uber_breakdown['2'].get(item,0) for item in uber_eta], color='orange', width=0.2)
# b3 = pylab.bar([1,2,3,4,5,6], [uber_breakdown['3'].get(item,0) for item in uber_eta], color='blue', width=0.1)
#
# pylab.legend([b1[0], b2[0], b3[0]], ['52 Bus -> Cali Train', '72 Bus -> Damen', 'UberX'])
# pylab.xticks([1,2,3,4,5,6], uber_eta)
#

def get_data(dataset):

    vec = DictVectorizer()
    arr = vec.fit_transform(dataset).toarray()

    return arr

def predict(X, Y):

    Y = np.array(Y)
    clf = MultinomialNB()
    clf.fit(X, Y)
    return clf.predict(X)

if __name__ == "__main__":

    vector = get_data(raw_routes_data)
    predictions = predict(vector, all_labels)

    m = metrics.classification_report(all_labels, predictions)
    print 'testing on 90/10 split'
    print m



    # ten_percent = len(raw_routes_data) / 10
    # print raw_routes_data[0]
    # # Training
    # training_label = all_labels[ten_percent:]
    # training_raw_data = raw_routes_data[ten_percent:]
    # training_data = DictVectorizer().fit_transform(training_raw_data).toarray()
    #
    #
    # learner = svm.LinearSVC()
    # learner.fit(training_data, training_label)
    #
    # # Predicting
    # testing_label = all_labels[:ten_percent]
    # testing_raw_data = raw_routes_data[:ten_percent]
    # testing_data = DictVectorizer().fit_transform(testing_raw_data).toarray()
    #
    # testing_predictions = learner.predict(testing_data)
    #
    #
    # m = metrics.classification_report(testing_label, testing_predictions)
    # print 'testing on 90/10 split'
    # print m
