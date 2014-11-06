import os
import json
from scripts import analytics_parser
from ga import initialize_service


SERVICE=initialize_service()

def write_analytics(url):

    kwargs = analytics_parser(url)

    data=SERVICE.data().ga().get(
                               ids=kwargs['ids'],
                               start_date=kwargs['start-date'],
                               end_date=kwargs['end-date'],
                               metrics=kwargs['metrics'],
                               dimensions=kwargs['dimensions'],
                               )
    data=data.execute()
    data = data.get('rows')
    with open('templates/data.json', 'w') as outfile:
      json.dump(data,outfile)

url = "https://www.googleapis.com/analytics/v3/data/ga?ids=ga:86930627&dimensions=ga:region&metrics=ga:pageviews&start-date=2014-10-01&end-date=2014-10-21"
write_analytics(url)
