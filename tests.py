import unittest
from analytics_proxy import *
import tempfile
import os
import json

from models import Proxy
from manage import initalize_database

class MyTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()


    def test_load_data(self):
        '''verify load_data, loads data properly'''
        load_data(
            endpoint="test_db",
            url="ids=ga:86930627&dimensions=ga:region&metrics=" + \
            "ga:pageviews&start-date=50daysAgo&end-date=today")

        #verify that data is in database
        test_proxy = Proxy.query.filter_by(endpoint="test_db").first()
        assert test_proxy.endpoint == "test_db"

        #verify that adding data with the same key updates database
        load_data(
            endpoint="test_db",
            url="https://www.googleapis.com/analytics/v3/data/ga?"+\
                "ids=ga:86930627&dimensions=ga:region&metrics="+\
                "ga:pageviews&start-date=99daysAgo&end-date=today",
            header=[['test_column_1'],['test_column_2']],
            rows=[['r1_c1','r1_c2'],['r2_c1','r2_c2']])
        test_proxy = Proxy.query.filter_by(endpoint="test_db").first()
        assert test_proxy.header[0][0] == "test_column_1"


    def test_api(self):
        '''verify api returns correct data'''
        r  = self.app.get('/api/test_db')
        assert r.status_code == 200
        data = json.loads(r.data)
        assert len(data['data']) == 4
        assert data['data'][0][0] == "test_column_1"


    def test_google_analytics_api(self):
        '''verify google api works'''
        specific_proxies = Proxy.query.filter_by(endpoint="test_db").all()
        process_analytics(specific_proxies=specific_proxies)
        r  = self.app.get('/api/test_db')
        data = json.loads(r.data)
        assert data['data'][0][0] != "test_column_1"


if __name__ == '__main__':
    unittest.main()
