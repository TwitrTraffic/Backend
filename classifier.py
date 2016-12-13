from flask import jsonify, abort, g, flash
from textblob.classifiers import NaiveBayesClassifier

train = [
    ('Slow Moving traffic', 'neg'),
    ('On going protest', 'neg'),
    ('Vehicles not allowed', 'neg'),
    ('Slow traffic', 'neg'),
    ('bus breakdown', 'neg'),
    ('expect traffic holdup', 'neg'),
    ('more rush', 'neg'),
    ('Traffic is restored', 'pos'),
    ('safe', 'pos'),
    ('normal', 'pos'),
    ('traffic cleared', 'pos'),
    ('Peak hour traffic', 'neu'),
    (' Routes to avoid', 'neu'),
    ('Traffic at', 'neu')
]


cl = NaiveBayesClassifier(train)


def classify(tweet):
    return cl.classify(tweet)


def getTweetsWithStatus(final):
    finalWithStatus = []

    neg = neu = pos = total = 0
    for tweet in final:
        inst = []
        inst.append(tweet[0])
        inst.append(tweet[1])
        inst.append(tweet[2])
        if classify(tweet[0]) == "neg":
            inst.append("Negative")
            neg = neg + 1
        elif classify(tweet[0]) == "pos":
            inst.append("Positive")
            pos = pos + 1
        elif classify(tweet[0]) == "neu":
            inst.append("Caution")
            neu = neu + 1
        finalWithStatus.append(inst)

    new_list = []
    temp = []
    inst = []
    total = neu + neg + pos

    inst.append((float(pos) / total) * 100)
    inst.append((float(neu) / total) * 100)
    inst.append((float(neg) / total) * 100)
    temp.append(inst)
    new_list = temp + finalWithStatus

    return new_list
