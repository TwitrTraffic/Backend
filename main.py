from flask import Flask,flash,render_template,redirect,url_for,jsonify,make_response,request,abort,g,flash
from helpers import getTwitterFeed,retrieveAllblrTweets,getCheckpoints,doActualWork,getCheckpointLocations
import sqlite3
from contextlib import closing


app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'aBcDeFg1@3$5'

# configuration
DATABASE = '/tmp/tt.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def connect_db():
    return sqlite3.connect(DATABASE)

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html')

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html'), 500

@app.route("/")
def mainInit():
	return render_template('home.html')

@app.route("/loadDb")
def loadDb():
	init_db()
	getTwitterFeed()
	return render_template('home.html')



#---------------------API Section-----------------------------------------------------------------------------------

#Sample API HIT: curl -i http://localhost:5000/api/blrttweets
@app.route("/api/blrttweets", methods=['GET'])
def blrttweets():
	tweets = retrieveAllblrTweets()
	return jsonify({'tweets': tweets}), 201
#----------------------------------------------------------------------------------------------------------------------------------


#Required Json: {
#				"src":"mvit",
#				"srclat":"40.81381340000001",
#				"srclong":"-74.06693179999999",
#				"dest":"hebbal",
#				"destlat":"40.8145647",
#				"destlong":"-74.06878929999999",
#				"day":"thursday",
#				"time":"13:32:12"
#				}


#Sample API HIT: curl -i -H "Content-Type: application/json" -X POST -d '{"src":"mvit","srclat":"40.81381340000001","srclong":"-74.06693179999999","dest":"hebbal","destlat":"40.8145647","destlong":"-74.06878929999999","day":"thursday","time":"13:32:12"}' http://localhost:5000/api/route
@app.route("/api/route", methods = ['POST'])
def inputRoute():
    if not request.json:
        abort(400)
    if "src" not in request.json:
    	abort(400)
    if "dest" not in request.json:
    	abort(400)	
    if "srclat" not in request.json:
    	abort(400)
    if "srclong" not in request.json:
    	abort(400)	
    if "destlat" not in request.json:
    	abort(400)
    if "destlong" not in request.json:
    	abort(400)	
    if "day" not in request.json:
    	abort(400)
    if "time" not in request.json:
    	abort(400)	
    
    #index '0'->lat ; '1'->long
    source = [request.json['srclat'],request.json['srclong'],request.json['src']]
    destination = [request.json['destlat'],request.json['destlong'],request.json['dest']]
    day = request.json['day']
    time = request.json['time']

    try:

        g.db.execute('insert into routes values (?, ?, ?, ?)',[source[2], destination[2], day, time])
        g.db.commit()

        g.db.execute('insert into coordinates values (?, ?, ?)',[source[2], source[0], source[1]])
        g.db.commit()

        g.db.execute('insert into coordinates values (?, ?, ?)',[destination[2], destination[0], destination[1]])
        g.db.commit()

    except sqlite3.IntegrityError:
        print "Could not add"

    loc = doActualWork(source,destination,day,time)

    

    return jsonify({"Under":"development","locations":loc}), 201
#----------------------------------------------------------------------------------------------------------------------------------


#Required Json: {
#				"srclat":"40.81381340000001",
#				"srclong":"-74.06693179999999",
#				"destlat":"40.8145647",
#				"destlong":"-74.06878929999999",
#				}


#Sample API HIT: curl -i -H "Content-Type: application/json" -X POST -d '{"srclat":"40.81381340000001","srclong":"-74.06693179999999","destlat":"40.8145647","destlong":"-74.06878929999999"}' http://localhost:5000/api/checkpoints
@app.route("/api/checkpoints", methods = ['POST'])
def checkpoints():
    if not request.json:
        abort(400)
    if "srclat" not in request.json:
    	abort(400)
    if "srclong" not in request.json:
    	abort(400)
    if "destlat" not in request.json:
    	abort(400)
    if "destlong" not in request.json:
    	abort(400)
    
    #index '0'->lat ; '1'->long
    source = [request.json['srclat'],request.json['srclong']]
    destination = [request.json['destlat'],request.json['destlong']]
    

    json_checkpoints = getCheckpoints(source,destination)
    locations = getCheckpointLocations(source,destination,"","")

    return jsonify({"checkpoints":locations}), 201


if __name__ == "__main__":
    app.run(debug = True)
