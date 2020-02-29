import json

def picker():
    jsopen = open('./static/instrument.json', 'r')
    jsload = json.load(jsopen)
