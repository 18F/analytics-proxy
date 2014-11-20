import json
from urlparse import urlparse
#from flask.ext.sqlalchemy import SQLAlchemy
from models import Proxy
from analytics_proxy import db


def analytics_parser(url):
    '''parses urls, and makes sure to convert "-" to "_" '''
    o = urlparse(url).query.split('&')
    kwargs = {}
    for element in o:
        element = element.split("=")
        kwargs[element[0].replace("-", "_")] = element[1]
    return kwargs


def call_api(url, SERVICE):
    '''calls api and returns result'''
    kwargs = analytics_parser(url)
    result = SERVICE.data().ga().get(**kwargs).execute()
    return result


def prepare_data(result):
    '''prepares data to return'''
    data = [[col['name'].strip("ga:") for col in result['columnHeaders']]]
    data.extend(result.get('rows'))
    return data


def load_data(endpoint, url, data=None):
    proxy = Proxy(endpoint=endpoint, url=url, data=data)
    db.session.merge(proxy)
    db.session.commit()


def initalize_database():
    with open('analytics_urls.txt') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip("\n").split("|")
        load_data(endpoint=line[0], url=line[0])


def update_database(endpoint, url, data=None):
    result = Proxy.query.filter_by(endpoint=endpoint, url=url).first()
    result.data = data
    db.session.commit()


def get_data(proxy_name="test1"):
    result = Proxy.query.filter_by(endpoint=proxy_name).first()
    if not result:
        return """{"Error":"No Data"}"""
    return result.data


def write_analytics(name, data):
    '''writes analytics to static file'''
    name = "templates/%s.json" % name
    with open(name, 'w') as outfile:
        json.dump(data, outfile)
