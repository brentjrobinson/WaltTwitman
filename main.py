import re
from pprint import pprint

import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
consumer_key = config['consumer_key']['key']
consumer_secret = config['consumer_secret']['key']
access_token = config['access_token_key']['key']
access_token_secret = config['access_token_secret']['key']


# This is a basic listener that just prints received tweets to stdout.


if __name__ == '__main__':
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)


    class MyStreamListener(tweepy.StreamListener):


        def on_error(self, status):
            print(status)

        def on_status(self, status):
            print(status.text)


    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    myStream.filter(languages=["en"], track=["a", "the", "i", "you", "u"])
