## Analytics Proxy

Analytics Proxy allows you to publicly share Google Analytics reporting data. It was partially inspired by [Google Analytics superProxy](https://github.com/googleanalytics/google-analytics-super-proxy); however, unlike [Google Analytics superProxy](https://github.com/googleanalytics/google-analytics-super-proxy) it doesn’t need to be deployed on [Google App Engine](https://appengine.google.com/)

## Setup

### Requirements
- [Postgres](http://www.postgresql.org/)
- [Python 2.7](https://docs.python.org/2/)
- [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html)
- [Redis](http://redis.io/) — currently running on sqlite

####Database Setup
After installing postgres:
```bash
createdb <name_of_database>
```

####Virtual Env
```bash
mkvirtualenv <name_of_env>
```

####Bash Settings
Start the virtualenv and edit the postactivate file
```bash
workon <name_of_env>
nano $VIRTUAL_ENV/bin/postactivate
```
and add the text below:
```bash
cd ~/<path_to_project>
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql://localhost/<name_of_database>”
```

####Initalizing Database Tables
```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

####Google Analytics Service Account
1. [Create Google API service account and take not of the client email](https://developers.google.com/accounts/docs/OAuth2ServiceAccount).
2.  Download the P12 private key file and place it in the analytics-proxy folder.
3.  Make sure to add the client email to the Google Analytics account.
3.  Update 'config.py' to include the client email and file name for the P12 private key
```python
 CLIENT_EMAIL = '<Your Client Email>'
 GA_P12_KEY = '<P12_private_key_file>'
```
