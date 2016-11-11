import tweepy,requests,sqlite3
import json,pprint,re
from flask import jsonify,abort,g,flash
from contextlib import closing
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
    
    while len(new_tweets) > 0 :
    #while t > 0:
        
        new_tweets = api.user_timeline('blrcitytraffic',count=200,max_id=oldest)
        
        alltweets.extend(new_tweets)
        
        oldest = alltweets[-1].id - 1

    
    for tweet in alltweets:
        if not tweet.retweeted and 'RT @' not in tweet.text:
            if '@' not in tweet.text: 
                #print "{}: {} -> {}".format(tweet.id,tweet.created_at,re.sub(r'[^\x00-\x7F]+',' ', tweet.text))
                dateTime = str(tweet.created_at).split()
                try:
                    g.db.execute('insert into tweets values (?, ?, ?, ?)',[tweet.id, str(re.sub(r'[^\x00-\x7F]+',' ', tweet.text)), dateTime[1], dateTime[0]])
                    g.db.commit()
                except sqlite3.IntegrityError:
                    print "Could not add"
                
   


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

def getCheckpointLocations(source,destination):
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

def insertRouteIntoDb(source,destination):
    locations = getCheckpointLocations(source,destination)

    delim = "|"
    locations_string = delim.join(locations)

    g.db.execute('insert into places values (?, ?, ?)',[source[2], destination[2], locations_string])
    g.db.commit() 

    #returning only for debugging
    return locations   


def getTrafficTweetsForRoute(locations,date,time):

    twittraffic = []

    time = []
    date = []
    places = []
    for loc in locations:
        places = places + ((loc.split(",")))

    places = list(set(places))
    
    place = [str(r) for r in places]


    for loction in locations:
        cmd = "select tweet,Ttime,Tdate from tweets where tweet like '%" + loction + "%' and Tdate='" + str(date) + "'order by Tdate desc"
        cur = g.db.execute(cmd)
        for row in cur.fetchall():
            inst = []
            inst.append(str(row[0]))
            inst.append(str(row[1]))
            inst.append(str(row[2]))
            twittraffic.append(inst)

    return twittraffic

def getTrafficTweetsForRouteAllTime(locations):

    twittraffic = []
    time = []
    date = []
    places = []
    for loc in locations:
        places = places + ((loc.split(",")))

    places = list(set(places))
    
    place = [str(r) for r in places]

    for loction in place:
        cmd = "select * from tweets where tweet like '%" + loction + "%'"
        cur = g.db.execute(cmd)
        for row in cur.fetchall():
            inst = []
            inst.append(str(row[1]))
            inst.append(str(row[2]))
            inst.append(str(row[3]))
            twittraffic.append(inst)
    twittraffic.sort(key=lambda x: x[2], reverse=True)
   
    return twittraffic