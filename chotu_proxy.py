#!chotu_proxy/bin/python
import os
import json
import re
from urlparse import urlparse

from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, render_template, jsonify
from extensions import initialize_service, make_celery

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
print os.environ['APP_SETTINGS']


#start celery
celery = make_celery(app)
celery.config_from_object('celeryconfig')
#start google service


'''SCRIPTS'''
def analytics_parser(url):
    o = urlparse(url).query.split('&')
    kwargs = {}
    for element in o:
        element = element.split("=")
        kwargs[element[0]] = element[1]
    return kwargs

def write_analytics(name, url, SERVICE):
    kwargs = analytics_parser(url)
    data=SERVICE.data().ga().get(
                               ids=kwargs['ids'],
                               start_date=kwargs['start-date'],
                               end_date=kwargs['end-date'],
                               metrics=kwargs['metrics'],
                               dimensions=kwargs['dimensions'],
                               ).execute()
    data = data.get('rows')
    name = "templates/%s.json" % name
    with open(name, 'w') as outfile:
        json.dump(data,outfile)


'''CELERY TASKS'''
@celery.task(name="tasks.process_analytics")
def process_analytics():
    SERVICE=initialize_service()
    print("service starts")
    with open('analytics_urls.txt') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip("\n").split("|")
        write_analytics(line[0],line[1],SERVICE)


'''ROUTES'''
@app.route("/write", methods = ['GET'])
def write_data():
	process_analytics.delay()
	return "writing api"


@app.route("/api/<proxy_name>", methods = ['GET'])
def get_api(proxy_name):
	with open('templates/%s.json' % proxy_name,'r') as infile:
		data = json.loads(infile.read())
	return jsonify(data)


if __name__ == '__main__':
    app.run(debug = True)
