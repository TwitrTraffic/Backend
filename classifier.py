from flask import jsonify,abort,g,flash
from textblob.classifiers import NaiveBayesClassifier

train = [
		('Slow Moving traffic', 'neg'),
		('Peak hour traffic', 'neg'),
		('On going protest', 'neg'),
		('Slow traffic', 'neg'),
		('bus breakdown', 'neg'),
		('expect traffic holdup', 'neg'),
		('more rush', 'neg'),
		('Traffic is restored', 'pos'),
		('traffic cleared', 'pos'),
		('Vehicles not allowed', 'neu'),
		(' Routes to avoid', 'neu'),
		('Traffic at', 'neu')
	]


cl = NaiveBayesClassifier(train)

def classify(tweet):
	print cl.classify(tweet)
	return cl.classify(tweet)

def getTweetsWithStatus(final):
	finalWithStatus = []
	for tweet in final:
		inst = []
		inst.append(tweet[0])
		inst.append(tweet[1])
		inst.append(tweet[2])
		if classify(tweet[0])=="neg":
			inst.append("Negative")
		elif classify(tweet[0])=="pos":
			inst.append("Positive")
		elif classify(tweet[0])=="neu":
			inst.append("Caution")
		finalWithStatus.append(inst)
	return finalWithStatus
