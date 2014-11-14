#!chotu_proxy/bin/python
import os
import json
from urlparse import urlparse

from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, render_template, jsonify

from extensions import *

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
print os.environ['APP_SETTINGS']

#start db
db = SQLAlchemy(app)
#start celery
celery = make_celery(app)
celery.config_from_object('celeryconfig')

from models import *

'''Scripts'''
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


def load_data(endpoint, url, data = None):
    '''load data into database'''
    proxy = Proxy(endpoint=endpoint, url=url, data=data)
    db.session.merge(proxy)
    db.session.commit()


def get_data(proxy_name="test1"):
    result = Proxy.query.filter_by(endpoint=proxy_name).first()
    if not result:
        return """{"Error":"No Data"}"""
    return jsonify(result.data)


'''CELERY TASKS'''
@celery.task(name="tasks.process_analytics")
def process_analytics():
    SERVICE= initialize_service()
    proxies = Proxy.query.all()
    for proxy in proxies:
        data = prepare_data(call_api(url=proxy.url, SERVICE=SERVICE))
        load_data(endpoint=proxy.endpoint,url=proxy.url,data=data)


'''ROUTES'''
@app.route("/write", methods = ['GET'])
def write_data():
    process_analytics()
    return "writing api"


@app.route("/api/<proxy_name>", methods = ['GET'])
@crossdomain(origin='*')
def get_api(proxy_name):
    return get_data(proxy_name)


@app.route("/api_direct/<agrs>", methods = ['GET'])
def get_api_direct(agrs):
    request_url = "http://127.0.0.1:5000/api_direct?%s" % agrs
    SERVICE= initialize_service()
    result = call_api(request_url, SERVICE)
    data = prepare_data(result)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug = True)
