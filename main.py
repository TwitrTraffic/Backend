from flask import Flask,flash,render_template,redirect,url_for,jsonify,make_response,request,abort,g,flash
from helpers import getTwitterFeed,retrieveAllblrTweets
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




#Sample API HIT: curl -i -H "Content-Type: application/json" -X POST -d '{"to":"mvit","from":"hebbal","day":"thursday","time":"13:32:12"}' http://localhost:5000/api/route
@app.route("/api/route", methods = ['POST'])
def inputRoute():
    if not request.json:
        abort(400)
    if "to" not in request.json:
    	abort(400)
    if "from" not in request.json:
    	abort(400)	
    
    source = request.json['to']
    destination = request.json['from']
    day = request.json['day']
    time = request.json['time']

    tasks=[]
    task = {
        'to': request.json['to'],
        'from': request.json['from']
    }
    tasks.append(task)

    return jsonify({'task': task}), 201


if __name__ == "__main__":
    app.run(debug = True)
