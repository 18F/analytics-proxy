from analytics_proxy import db
from sqlalchemy.dialects.postgresql import JSON

class Proxy(db.Model):
    __tablename__ = 'proxies'

    endpoint = db.Column(db.String(), primary_key=True)
    url = db.Column(db.String(), nullable=False, unique=True)
    header = db.Column(JSON, nullable=True)
    rows = db.Column(JSON, nullable=True)

    def __init__(self, endpoint, url, header = None, rows = None):
        self.endpoint = endpoint
        self.url = url
        self.header = header
        self.rows = rows

    def __repr__(self):
        return '<endpoint {}>'.format(self.endpoint)
