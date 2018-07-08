import re
import string
from pprint import pprint

import tweepy
from tweepy import OAuthHandler
from rhyme import rhymes
import pronouncing
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
consumer_key = config['consumer_key']['key']
consumer_secret = config['consumer_secret']['key']
access_token = config['access_token_key']['key']
access_token_secret = config['access_token_secret']['key']


class Tweet(object):
    def __init__(self, content, id):
        self.content = content
        self.id = id
        self.rhymeword = None
        self.rhyminglist = []

    def get_rhyme(self):
        list = self.content.strip()
        result = re.sub(r"http\S+", "", list)
        result = re.sub(r'[^\w\s]', '', result)
        last = result.rsplit(None, 1)[-1]
        last.translate(string.punctuation)
        self.rhymeword = last


if __name__ == '__main__':

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)


    class MyStreamListener(tweepy.StreamListener):

        def on_error(self, status):
            print(status)

        # def on_status(self, status):
        #     #print(status.text)


    potential = []
    myStreamListener = MyStreamListener()
    for tweet in tweepy.Cursor(api.search, q='pythonK', tweet_mode='extended', lang='en').items(2000):
        # Defining Tweets Creators Name
        tweettext = str(tweet.full_text.lower().encode('ascii',
                                                       errors='ignore'))
        # Defining Tweets Id
        tweetid = tweet.id

        # printing the text of the tweet

        tweet = Tweet(tweettext, tweetid)
        tweet.get_rhyme()
        tweet.rhyminglist = rhymes(tweet.rhymeword)
        if not tweet.rhyminglist:
            print("NO Found rhymes")
        elif len(tweet.rhymeword) > 4:
            print("Found rhymes")
            potential.append(tweet)
        if len(potential) > 100:
            break

    couplets = []

    print('/' * 80)

    for tweets in potential:
        print (tweets.content)
    print('/' * 80)
    for i in range(len(potential)-1, -1, -1):
        check = potential[i].rhymeword
        j = len(potential)-1
        while j >=0 :
            if check in potential[j].rhyminglist:
                print(potential[i].content)
                print(potential[j].content)
                del potential[j]
            j -= 1



