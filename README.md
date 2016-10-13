# Backend
Flask server for APIs

1) install requirements:	pip install -r requirements.txt

2) git clone the repo

3) run the flask web app: 	cd backend; python main.py;

4) 3) check localhost:		http://localhost:5000 OR http://127.0.0.1:5000



---------
#APIs

- Send dummy Json with 'to', 'from', 'day' and 'time' fields and get back same data (intentional, for now)
```curl -i -H "Content-Type: application/json" -X POST -d '{"to":"mvit","from":"hebbal","day":"thursday","time":"13:32:12"}' http://localhost:5000/api/route```

- To retrieve all tweets from blrtraffic twitter feed
```curl -i http://localhost:5000/api/blrttweets```

	