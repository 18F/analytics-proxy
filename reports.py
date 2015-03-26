
report_dict = [
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
    },
    {
        'report_name': 'top-countries',
        'refresh_rate': 60,
        'query': {
            'ids': 'ga:86930627',
            'dimensions': 'ga:country',
            'metrics': 'ga:sessions',
            'start_date': '2013-11-20',
            'end_date': '2015-11-30'
        }
    }

]
