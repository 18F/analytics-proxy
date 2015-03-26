import os
import redis
import pickle

from flask import Flask, Response, jsonify

from ga_functions import initialize_service, call_api, prepare_data

app = Flask(__name__)
app.config.from_object(os.getenv('APP_SETTINGS'))
app.redis = redis.StrictRedis(host=app.config['REDIS_HOST'], port=6379, db=0)


@app.route("/", methods=['GET'])
def index():
    return "Project Info"


@app.route("/data/<report_name>", methods=['GET'])
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

    call_dict = [
        {
            'report_name': 'top-sources',
            'refresh_rate': 60,
            'query': {
                'ids': 'ga:86930627',
                'dimensions': 'ga:source',
                'metrics': 'ga:sessions',
                'start_date': '2013-11-20',
                'end_date': '2015-11-30'
            }
        },
        {
            'report_name': 'top-pages',
            'refresh_rate': 60,
            'query': {
                'ids': 'ga:86930627',
                'dimensions': 'ga:pageTitle',
                'metrics': 'ga:sessions',
                'start_date': '2013-11-20',
                'end_date': '2015-11-30'
            }
        }
    ]
    for item in call_dict:
        print(item.get('report_name'), " added")
        app.redis.set(item['report_name'], pickle.dumps(item))
    app.run(host='0.0.0.0', port=port)
