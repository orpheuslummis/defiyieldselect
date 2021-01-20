"""
exposing the results

/latest
/TBD (obtain specific intervals)
"""

from flask import Flask

from dfo.config import HOST, PORT
from dfo.db import latest_scores, prepared_db

database = prepared_db()
app = Flask(__name__)


# @app.before_request
# def _db_connect():
#     database.connect()


# @app.teardown_request
# def _db_close(exc):
#     if not database.is_closed():
#         database.close()


@app.route('/dfo/results/latest')
def results_latest() -> dict:
    return {'results': latest_scores()}


@app.route('/')
def healthcheck() -> str:
    return 'ok'


def run() -> None:
    app.run(port=PORT, host=HOST)
