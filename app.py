# -*- coding: utf-8 -*-
"""
    jQuery Example
    ~~~~~~~~~~~~~~

    A simple application that shows how Flask and jQuery get along.

    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import requests
from flask import Flask, jsonify, render_template, request
import numpy as np
import time

app = Flask(__name__)

api_url = 'http://ck-hackday.us-east-1.elasticbeanstalk.com/medline/'

session = requests.Session()
session.cookies.get_dict()
response = session.get('http://ck-hackday.us-east-1.elasticbeanstalk.com/medline/auth')
cookie = session.cookies.get_dict()

def getyears(textdict, yrmax):
	n = len(textdict['results'])
	yrcount = np.zeros(yrmax)
	for i in range(n):
        	timestamp = float(textdict['results'][i]['pubdate'])
		tm = time.gmtime(timestamp / 1000.0)
		#print i, tm[0]
		yrcount[tm[0]-1] += 1
	k = np.count_nonzero(yrcount)
	yrdict = [dict() for x in range(k)]
	cntr = 0
	for i in range(yrmax):
		if yrcount[i]>0:
			yrdict[cntr]["year"] = i+1
			yrdict[cntr]["count"] = yrcount[i]
			cntr += 1

	return yrdict

@app.route('/search/<term>')
def search(term):
    r = requests.get(api_url + 'search/' + term, cookies=cookie)
    mydict = r.json()
    mydict['yeardata'] = getyears(mydict, 2016)
    # return mydict
    return jsonify(mydict)


@app.route('/_add_numbers')
def add_numbers():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
