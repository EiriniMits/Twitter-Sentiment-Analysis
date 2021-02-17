from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
import csv
import json
import re

# add your keys

access_token = ""
access_secret = ""
consumer_key = ""
consumer_secret = ""

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

file_name = 'Trump.csv'
with open(file_name, 'a', newline='') as csvfile:
    csv_writer = csv.DictWriter(
        f=csvfile,
        fieldnames=["Publised", "Tweet", "Sentiment", "Confidence"]
    )
    csv_writer.writeheader() # write the first row of csv file
csvfile.close()


class MyListener(StreamListener):

    def clean_tweet(self, tweet): #clean the tweets
        x = re.sub(r"http\S+", "", tweet)
        x = re.sub('[^A-Za-z0-9]+', ' ', x)
        return x

    def on_data(self, data):
        tweet = json.loads(data) #convert the tweet into a json format
        file_name = 'Trump.csv'
        with open(file_name, 'a', newline='') as csvfile:
            csv_writer = csv.DictWriter(
                f=csvfile,
                fieldnames=["Publised", "Tweet",  "Sentiment", "Confidence"]
            )
            if not tweet['retweeted'] and 'RT @' not in tweet['text']: #ignore retweets
                if 'extended_tweet' in tweet:
                    analysis = TextBlob(self.clean_tweet(tweet['extended_tweet']['full_text']))
                    text = tweet['extended_tweet']['full_text'].encode('ascii', 'ignore')
                    print(">>>[" + tweet['created_at'] + " : " + tweet['extended_tweet']['full_text'].replace('\n','') + "]<<< ")
                else:
                    analysis = TextBlob(self.clean_tweet(tweet['text']))
                    text = tweet['text'].encode('ascii', 'ignore')
                    print(">>>[" + tweet['created_at'] + " : " + tweet['text'].replace('\n','') + "]<<< ")
                if analysis.sentiment.polarity > 0:
                    sentiment = 'positive'
                elif analysis.sentiment.polarity == 0:
                    sentiment = 'neutral'
                else:
                    sentiment = 'negative'
                csv_writer.writerow({
                    'Publised': tweet['created_at'],
                    'Tweet':  text,
                    'Sentiment': sentiment,
                    'Confidence': analysis.sentiment.subjectivity
                })
        return True

    def on_error(self, status):
        print(status)
        return True


twitter_stream = Stream(auth, MyListener(), tweet_mode='extended')
twitter_stream.filter(track=["#Trump"],languages=['en'])
