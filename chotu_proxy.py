#!chotu_proxy/bin/python
import os
import json
import settings
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, render_template, jsonify
from extensions import initialize_service, make_celery
from scripts import analytics_parser

app = Flask(__name__)
app.config.from_object(settings)

#app.config.from_object(os.environ['APP_SETTINGS'])
#print os.environ['APP_SETTINGS']

#start google service
SERVICE=initialize_service()
#start celery
celery = make_celery(app)


@celery.task(name="tasks.write_analytics")
def write_analytics(url=None):
	url = "https://www.googleapis.com/analytics/v3/data/ga?ids=ga:86930627&dimensions=ga:region&metrics=ga:pageviews&start-date=2013-10-01&end-date=2014-10-21"
	kwargs = analytics_parser(url)

	data=SERVICE.data().ga().get(
                               ids=kwargs['ids'],
                               start_date=kwargs['start-date'],
                               end_date=kwargs['end-date'],
                               metrics=kwargs['metrics'],
                               dimensions=kwargs['dimensions'],
                               ).execute()
	data = data.get('rows')
	with open('templates/data.json', 'w') as outfile:
		json.dump(data,outfile)


@app.route("/write", methods = ['GET'])
def write_data():
	write_analytics.delay()
	return "writing api"


@app.route("/get", methods = ['GET'])
def get_api():
	with open('templates/data.json','r') as infile:
		data = json.loads(infile.read())
	return jsonify(data)

if __name__ == '__main__':
    app.run(debug = True)
