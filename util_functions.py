import pickle

from oauth2client.client import SignedJwtAssertionCredentials
from httplib2 import Http
from apiclient.discovery import build
from flask import make_response, request, current_app
from datetime import timedelta
from functools import update_wrapper


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
    """ calls api and returns result """
    result = service.data().ga().get(**query).execute()
    return result


def prepare_data(result):
    """ Prepares data to return """
    header = [col['name'].strip("ga:") for col in result['columnHeaders']]
    data = []
    for row in result.get('rows'):
        data.append(dict(zip(header, row)))
    return {'data': data}


def load_reports(redis_client):
    """ Loads reports into redis """
    from reports import report_dict
    for item in report_dict:
        redis_client.set(item['report_name'], pickle.dumps(item))


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator
