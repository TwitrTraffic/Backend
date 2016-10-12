import tweepy
import json,pprint,re
from flask import jsonify,abort,g,flash
import sqlite3
from contextlib import closing



consumer_key = "0k8uoadFwyNdrof19BVZ1arm2"
consumer_secret = "DJo51iWuWd40eyI1Cg2W5BEJRHGJTKedfC8nxiFzTBZhpv3XuC"
access_token = "785716793432166401-NfwBGuujsq9lbds3eTA5Jt6TdDomZUA"
access_token_secret = "lIQGgZ9Dg5DbCdWQmYnJLlGbLq3vFnHgP147Kz4uCrcg9"



def getTwitterFeed():   

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    
    alltweets = []

    new_tweets = api.user_timeline('blrcitytraffic',count=200)
    alltweets.extend(new_tweets)

    oldest = alltweets[-1].id - 1
    t=1
    #while len(new_tweets) > 0:
    while t > 0:
        t=t-1
        new_tweets = api.user_timeline('blrcitytraffic',count=10,max_id=oldest)
        
        alltweets.extend(new_tweets)
        
        oldest = alltweets[-1].id - 1

    k=1
    for tweet in alltweets:
        if not tweet.retweeted and 'RT @' not in tweet.text:
            if '@' not in tweet.text: 
                print "{}: {} -> {}".format(tweet.id,tweet.created_at,re.sub(r'[^\x00-\x7F]+',' ', tweet.text))
                dateTime = str(tweet.created_at).split()
                g.db.execute('insert into tweets(tweet,Ttime,Tdate) values (?, ?, ?)',[str(re.sub(r'[^\x00-\x7F]+',' ', tweet.text)), dateTime[1], dateTime[0]])
                g.db.commit()
                k=k+1

    cur = g.db.execute('select tweet from tweets')
    entries = cur.fetchall()
    return entries


def retrieveAllblrTweets():
    cur = g.db.execute('select * from tweets')
    entries = [dict(id=row[0], tweet=row[1], time=row[2], date=row[3]) for row in cur.fetchall()]
    return entries