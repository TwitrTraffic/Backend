import tweepy
import json,pprint,re
from flask import jsonify,abort,g,flash
import sqlite3
from contextlib import closing
import requests
from urllib2 import urlopen
from keys import GoogleApiKey,twitter_consumer_key,twitter_consumer_secret,twitter_access_token,twitter_access_token_secret

YOUR_API_KEY = GoogleApiKey

consumer_key = twitter_consumer_key
consumer_secret = twitter_consumer_secret
access_token = twitter_access_token
access_token_secret = twitter_access_token_secret



def getTwitterFeed():   

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    
    alltweets = []

    new_tweets = api.user_timeline('blrcitytraffic',count=200)
    alltweets.extend(new_tweets)

    oldest = alltweets[-1].id - 1
    t = 30
    while len(new_tweets) > 0 and t > 0:
    #while t > 0:
        t=t-1
        new_tweets = api.user_timeline('blrcitytraffic',count=200,max_id=oldest)
        
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

def getCheckpoints(source,destination):
	url = 'https://maps.googleapis.com/maps/api/directions/json?origin=12.9577133,77.6852271&destination=14.0187447,75.2582987&key=' + YOUR_API_KEY
	response = urlopen(url)
	json_obj = json.load(response)

	json_routes = json_obj['routes']

	for i in json_routes:
		json_legs = i['legs']

	for i in json_legs:
		json_steps = i['steps']

	json_checkpoints = []

	for i in json_steps:
		json_checkpoints.append(i['end_location'])

	#print json.dumps(json_checkpoints,indent=2)

	return json_checkpoints

def getCheckpointLocations(source,destination,day,time):
	json_checkpoints = getCheckpoints(source,destination)

	json_checkpoint_locations = []

	for i in json_checkpoints:
		url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=' + str(i['lat']) + ','+ str(i['lng']) + '&key=' + YOUR_API_KEY
		response = urlopen(url)
		json_obj = json.load(response)
		results = json_obj['results']

		addr_component = results[0]
		address = addr_component['formatted_address']
		json_checkpoint_locations.append(address)

	return json_checkpoint_locations

def doActualWork(source,destination,day,time):
    location_addr = getCheckpointLocations(source,destination,day,time)

    locations = []
    loc_comp = []
    for loc in location_addr:
        loc_comp = loc.split(',')
        locations.append(loc_comp[0])

    delim = ","
    locations_string = delim.join(locations)

    g.db.execute('insert into places values (?, ?, ?)',[source[2], destination[2], locations_string])
    g.db.commit()    

    twittrafic = []

    for loction in locations:
        cmd = "select tweet from tweets where tweet like '%" + loction + "%'"
        cur = g.db.execute(cmd)
        
        #entries = []
        for row in cur.fetchall():
            twittrafic.append(row)


    return twittrafic