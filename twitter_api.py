import requests
from requests_oauthlib import OAuth1
import json
from serializers import Tweet
from settings import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET

class Twitter(object):
    BASE_URL = "https://api.twitter.com/1.1/"
    def __init__(self, consumer_key=None, consumer_secret=None, oauth_token=None, oauth_secret=None):
        self.consumer_key = consumer_key or TWITTER_CONSUMER_KEY
        self.consumer_secret = consumer_secret or TWITTER_CONSUMER_SECRET
        self.oauth_token = oauth_token or OAUTH_TOKEN
        self.oauth_token_secret = oauth_secret or OAUTH_TOKEN_SECRET
        self.auth=OAuth1(self.consumer_key,
                         client_secret=self.consumer_secret,
                         resource_owner_key=self.oauth_token,
                         resource_owner_secret=self.oauth_token_secret)

    def get_user_timeline(self, user_id, screen_name):

        request_url = self.BASE_URL + "statuses/user_timeline.json?include_rts=false&exclude_replies=true&count=200"

        if screen_name:
            request_url += "&screen_name={0}".format(screen_name)
        elif user_id:
            request_url += "&user_id={0}".format(user_id)

        timeline_data = requests.get(request_url, auth=self.auth)

        return [Tweet(**tweet) for tweet in json.loads(timeline_data.content)]