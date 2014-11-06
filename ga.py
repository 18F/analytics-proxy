from oauth2client.client import SignedJwtAssertionCredentials
from httplib2 import Http
from apiclient.discovery import build

def initialize_service():
    '''initalizes google analytics service'''
    client_email = '556009582678-d1er91t08n95fg8ldvaojdric02pqd8u@developer.gserviceaccount.com'
    with open("ramirez_key.p12") as f:
      private_key = f.read()
    credentials = SignedJwtAssertionCredentials(client_email, private_key,
        'https://www.googleapis.com/auth/analytics.readonly')
    http_auth = credentials.authorize(Http())

    return build('analytics', 'v3', http=http_auth)
