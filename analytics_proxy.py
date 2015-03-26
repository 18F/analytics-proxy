import os
import redis
import pickle

from flask import Flask, Response, jsonify

from util_functions import (
    initialize_service, call_api, prepare_data, load_reports, crossdomain)

app = Flask(__name__)
app.config.from_object(os.getenv('APP_SETTINGS'))
app.redis = redis.StrictRedis(host=app.config['REDIS_HOST'], port=6379, db=0)
load_reports(app.redis)


@app.route("/", methods=['GET'])
def index():
    return "Project Info"


@app.route("/data/<report_name>", methods=['GET'])
@crossdomain(origin='*')
def get_analytics(report_name):

    report = app.redis.get(report_name)
    if not report:
        response = Response(
            "{'error': 'No Report'}",
            status=200,
            mimetype='application/json'
        )
    else:
        report = pickle.loads(report)
        redis_data = app.redis.get(report_name + '_data')
        if not redis_data:
            ga_api_service = initialize_service(app.config)
            data = prepare_data(
                call_api(query=report['query'], service=ga_api_service))
            app.redis.set(report_name + '_data', pickle.dumps(data))
            app.redis.expire(report_name + '_data', report['refresh_rate'])
        else:
            data = pickle.loads(redis_data)

        data['report'] = report
        response = jsonify(data)

    return response


if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
