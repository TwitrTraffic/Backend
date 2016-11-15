import sqlite3,csv
from flask import g

def exportLocations():
	data = g.db.execute('select * from places;')
	with open('reports/locations.csv', 'wb') as f:
	    writer = csv.writer(f)
	    writer.writerow(['Source', 'Destination', 'Checkpoints'])
	    writer.writerows(data)

def exportTweets():
	data = g.db.execute('select tweet,Ttime,Tdate from tweets;')
	with open('reports/tweets.csv', 'wb') as f:
	    writer = csv.writer(f)
	    writer.writerow(['Tweet', 'Time', 'Date'])
	    writer.writerows(data)

def exportRoute():
	data = g.db.execute('select tweet,Ttime,Tdate from tweets;')
	with open('reports/tweets.csv', 'wb') as f:
	    writer = csv.writer(f)
	    writer.writerow(['Tweet', 'Time', 'Date'])
	    writer.writerows(data)