
import re
from urlparse import urlparse

def analytics_parser(url):
    o = urlparse(url).query.split('&')
    kwargs = {}
    for element in o:
        element = element.split("=")
        kwargs[element[0]] = element[1]
    return kwargs
