#!/usr/bin/python

from twitter import OAuth, TwitterStream
from datetime import datetime, timedelta


def twitter_stream():
    config = {}
    hashtags = {}  # 'hashtag': 'count'
    execfile('config.py', config)
    auth = OAuth(config['access_key'], config['access_secret'],
                 config['consumer_key'], config['consumer_secret'])
    stream = TwitterStream(auth=auth, secure=True)
    tweet_iter = stream.statuses.sample()
    start_time = datetime.now()
    for tweet in tweet_iter:
        if datetime.now() > start_time + timedelta(minutes=10):
            break
        if 'entities' in tweet:
            for h in tweet['entities']['hashtags']:
                if h['text'] not in hashtags:
                    hashtags[h['text']] = 1
                else:
                    hashtags[h['text']] += 1
    print '{}\t{}'.format(datetime.now() - timedelta(minutes=10), datetime.now())
    sorted_hashtags = sorted(hashtags.items(), key=lambda x: x[1], reverse=True)
    for h in sorted_hashtags[:10]:
        print h[0],
        print '\t{}'.format(h[1])


if __name__ == '__main__':
    twitter_stream()
