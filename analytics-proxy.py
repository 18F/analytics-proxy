#!chotu_proxy/bin/python
import os
import json
import re
import datetime
import logging

from urlparse import urlparse

from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, render_template, jsonify
from extensions import *

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
print os.environ['APP_SETTINGS']

#start celery
celery = make_celery(app)
celery.config_from_object('celeryconfig')


'''SCRIPTS'''
def analytics_parser(url):
    '''parses urls, and makes sure to convert "-" to "_" '''
    o = urlparse(url).query.split('&')
    kwargs = {}
    for element in o:
        element = element.split("=")
        kwargs[element[0].replace("-","_")] = element[1]
    return kwargs


def call_api(url, SERVICE):
    '''calls api and returns result'''
    kwargs = analytics_parser(url)
    result=SERVICE.data().ga().get(**kwargs).execute()
    return result


def prepare_data(result):
    '''prepares data to return'''
    data = [[col['name'].strip("ga:") for col in result['columnHeaders']]]
    data.extend(result.get('rows'))
    return data


def write_analytics(name, url, SERVICE):
    '''writes analytics to static file'''
    result = call_api(url, SERVICE)
    data = prepare_data(result)
    name = "templates/%s.json" % name
    with open(name, 'w') as outfile:
        json.dump(data,outfile)


'''CELERY TASKS'''
@celery.task(name="tasks.process_analytics")
def process_analytics():
    SERVICE= initialize_service()
    with open('analytics_urls.txt') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip("\n").split("|")
        write_analytics(line[0],line[1],SERVICE)


'''ROUTES'''
@app.route("/write", methods = ['GET'])
def write_data():
    process_analytics()
    return "writing api"


@app.route("/api/<proxy_name>", methods = ['GET'])
@crossdomain(origin='*')
def get_api(proxy_name):
  with open('templates/%s.json' % proxy_name,'r') as infile:
    data =infile.read()
  return data

@app.route("/api_direct/<agrs>", methods = ['GET'])
def get_api_direct(agrs):
    request_url = "http://127.0.0.1:5000/api_direct?%s" % agrs
    SERVICE= initialize_service()
    result = call_api(request_url, SERVICE)
    data = prepare_data(result)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug = True)
