#!superproxy/bin/python

from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, render_template, jsonify
import os
import json
from celery import Celery
from make_celery import make_celery
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
#print os.environ['APP_SETTINGS']

celery = make_celery(app)

@celery.task()
def add_together(a,b):
  with open("test.txt", "w") as f:
    f.write("test")
  return a + b

@app.route("/get", methods = ['GET'])
def get_analytics():

    print add_together.delay(1,1)
    with open('templates/data.json','r') as infile:
      data = json.loads(infile.read())
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug = True)
