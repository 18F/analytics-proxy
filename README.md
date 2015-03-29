## Analytics Proxy

Analytics Proxy allows you to publicly share Google Analytics reporting data. It was partially inspired by [Google Analytics superProxy](https://github.com/googleanalytics/google-analytics-super-proxy); however, unlike [Google Analytics superProxy](https://github.com/googleanalytics/google-analytics-super-proxy) it doesn’t need to be deployed on [Google App Engine](https://appengine.google.com/)

## Setup

### Requirements
- [Python 2.7](https://docs.python.org/2/)
- [Redis](http://redis.io/)

### Google Analytics Service Account
1. [Create Google API service account and take not of the client email](https://developers.google.com/accounts/docs/OAuth2ServiceAccount).
2.  Download the P12 private key file and place it in the analytics-proxy folder.
3.  Make sure to add the client email to the Google Analytics account.

### Install Redis
```bash
# Mac OS
brew install redis
# Ubuntu
sudo apt-get install redis-server
```

### Start Redis
```
redis-server
```

### Env Variables
```
export APP_SETTINGS="app_config.DevelopmentConfig"
export CLIENT_EMAIL=<<GA CLIENT_EMAIL>>
export GA_P12_KEY=<<Location of P12 Key>>
```

### Modify `reports.py` to meet reporting needs.
```
    {
        'report_name': 'top-sources',
        'refresh_rate': 60,
        'query': {
            'ids': 'ga:<<your ga:ID>>',
            'dimensions': 'ga:source',
            'metrics': 'ga:sessions',
            'start_date': '2013-11-20',
            'end_date': '2015-11-30'
        }
    },
```
