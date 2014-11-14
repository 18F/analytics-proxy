from analytics_proxy import db
from sqlalchemy.dialects.postgresql import JSON

class Proxy(db.Model):
    __tablename__ = 'proxies'

    endpoint = db.Column(db.String(), primary_key=True)
    url = db.Column(db.String(), nullable=False, unique=True)
    data = db.Column(JSON, nullable=True)

    def __init__(self, endpoint, url, data = None):
        self.endpoint = endpoint
        self.url = url
        self.data = data

    def __repr__(self):
        return '<endpoint {}>'.format(self.endpoint)
