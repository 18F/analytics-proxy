from oauth2client.client import SignedJwtAssertionCredentials
from httplib2 import Http
from apiclient.discovery import build
from time import time


def initialize_service(config):
    """ Initalizes google analytics service """

    client_email = config['CLIENT_EMAIL']
    with open(config['GA_P12_KEY'], 'r') as f:
        private_key = f.read()
    credentials = SignedJwtAssertionCredentials(
        client_email, private_key,
        'https://www.googleapis.com/auth/analytics.readonly')
    http_auth = credentials.authorize(Http())

    return build('analytics', 'v3', http=http_auth)


def call_api(query, service):
    '''calls api and returns result'''
    result = service.data().ga().get(**query).execute()
    return result


def prepare_data(result):
    '''prepares data to return'''
    header = [col['name'].strip("ga:") for col in result['columnHeaders']]
    data = []
    for row in result.get('rows'):
        data.append(dict(zip(header, row)))
    return {'data': data}
