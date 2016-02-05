import csv
import operator
from serializers import Tweet
from datetime import datetime, timedelta
import pylab
import re
from dateutil import tz

all_tweets = {}
all_ids = set([])

def ngrams(input, n):
    input = input.split(' ')
    output = []
    for i in range(len(input)-n+1):
        output.append(input[i:i+n])

    return output

with open("/Users/lorenamesa/Desktop/pytennessee/cta_tweet_data.csv", "r") as csvdata:
    headers = ['id_str', 'created_at', 'text']
    reader = csv.reader(csvdata)

    for row in reader:
        if len(row) == 3:
            data = dict(zip(headers, row))
            tweet = Tweet(**data)
            if not all_tweets.get(tweet.tweet_id):
                all_tweets[tweet.tweet_id] = tweet
            else:
                all_tweets[tweet.tweet_id] = tweet

        # print datetime.datetime.strptime(tweet.created_at, "%Y%m%d %H:%M")  # local time
        # print bus_prediction.get_requested_time_hr()

    print len(all_tweets) # 262

    all_tweet_bigrams = [ngrams(re.sub(r'[^\w\s]', '', data.text), 2) for tweet_id, data in all_tweets.iteritems()]
    all_tweet_bigrams = sum(all_tweet_bigrams, [])

    bigrams_freq = {}

    for bigram in all_tweet_bigrams:
        joined_bigram = ' '.join(bigram)
        if joined_bigram not in bigrams_freq:
            bigrams_freq[joined_bigram] = 1
        else:
            bigrams_freq[joined_bigram] += 1

    sorted_bigrams_freq = sorted(bigrams_freq.items(), key=operator.itemgetter(1), reverse=True)
    print sorted_bigrams_freq[:10] # [('trains are', 112), ('Line trains', 100), ('are operating', 70), ('residual delays', 67), ('delays after', 67), ('operating with', 67), ('with residual', 65), ('due to', 60), ('buses are', 50), ('rerouted via', 50)]

    labels = [bigram[0] for bigram in sorted_bigrams_freq[:10]]
    data = [bigram[1] for bigram in sorted_bigrams_freq[:10]]
    pylab.title('Top 10 Bigrams in CTA Tweet Data January 2016')
    pylab.pie(data, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    pylab.show()

    relevant_tweets = []

    for tweet_id, data in all_tweets.iteritems():
        if "blue" in data.text.lower() and "residual delay" in data.text.lower(): #and "O'Hare" not in data.text.lower():
            print data.created_at # Fri Jan 29 05:34:56 +0000 2016
            print datetime.strptime(data.created_at, "%a %b %d %H:%M:%S +0000 %Y").replace(tzinfo=tz.tzlocal()), data.text
            utctimestamp = int((datetime.strptime(data.created_at, "%a %b %d %H:%M:%S +0000 %Y") - datetime(1970, 1, 1)).total_seconds())
            data.created_at = utctimestamp
            # print data.created_at
            relevant_tweets.append(data)
        if "72 north" in data.text.lower():
            utctimestamp = int((datetime.strptime(data.created_at, "%a %b %d %H:%M:%S +0000 %Y") - datetime(1970, 1, 1)).total_seconds())
            data.created_at = utctimestamp
            relevant_tweets.append(data)
        if "52 kedzie/california" in data.text.lower() and "delay" in data.text.lower():
            utctimestamp = int((datetime.strptime(data.created_at, "%a %b %d %H:%M:%S +0000 %Y") - datetime(1970, 1, 1)).total_seconds())
            data.created_at = utctimestamp
            relevant_tweets.append(data)

    # pylab.title("Range of Damen Blue Line Train ETAs in January 2016 From Home to Work Between 6am to 12pm")
    # pylab.legend(loc='best')
    # pylab.xlabel("Train Delayed")
    # pylab.ylabel("Number of Trains")
    # pylab.plot()
    # pylab.show()


with open("/Users/lorenamesa/Desktop/pytennessee/tweet_labeled_data.csv", "w") as csvdata:
    headers = ['created_at', 'tweet_id', 'text']

    writer = csv.writer(csvdata, dialect='excel')
    writer.writerow(headers)

    for tweet in relevant_tweets:
        writer.writerow([tweet.created_at, tweet.tweet_id, tweet.text])


