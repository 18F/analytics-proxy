## Analytics Proxy

Analytics Proxy is allows you to publicly share your Google Analytics reporting data. It was partially inspired by [Google Analytics superProxy](https://github.com/googleanalytics/google-analytics-super-proxy). However, unlike [Google Analytics superProxy](https://github.com/googleanalytics/google-analytics-super-proxy) it doesn’t have to be deployed on [Google App Engine](https://appengine.google.com/)

## Setup

### Requirements 
- [Postgres](http://www.postgresql.org/)
- [Python 2.7](https://docs.python.org/2/)
- [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html)
- [Redis](http://redis.io/) — currently running on sqlite 

###Bash Settings
Open the “postactivate” file with:
```bash
nano $VIRTUAL_ENV/bin/postactivate
```
and add the text below:
```bash
cd ~/<path_to_project>
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql://localhost/<name_of_database>”
```