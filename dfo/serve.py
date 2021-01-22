"""
exposing the results

/latest
/TBD (obtain specific intervals)
"""

from flask import Flask
from gevent.pywsgi import WSGIServer

from dfo.config import DEBUG, HOST, PORT
from dfo.db import latest_results

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/dfo/results/latest')
def results_latest() -> dict:
    return {'results': latest_results()}


@app.route('/')
def healthcheck() -> str:
    return 'ok'


def run() -> None:
    if not DEBUG:
        http_server = WSGIServer((HOST, PORT), app)
        http_server.serve_forever()
    else:
        app.run(port=PORT, host=HOST)
