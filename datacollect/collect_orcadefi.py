import csv
import logging
import os
import sched
import sys
import time

import requests


logging.basicConfig(format='{asctime} - {name} - {levelname} - {message}', style='{')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


INTERVAL = 60
PATH = "/data/"
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjMyNDU2MSIsIm5hbWUiOiJNaXJvc2xhdiIsImlhdCI6Nzg5NDUyMTIzNTZ9.GQ5LR3jdhmTl_rmKgNPzrgNRrx9nflhJBiEgjz5Coec'
API_URL = "http://orcadefi.com:10000/api/v1/realtime/"


def collect_data(token):
    query = f"{API_URL}all?token={token}"

    try:
        response = requests.get(url=query)
        platforms_items = response.json().items()

        for key_platform, val in platforms_items:
            # Iterate over every pair for each platform 
            platform = val['Platform']
            measurement = val['_measurement']
            start = val['_start']
            stop = val['_stop']

            for pair, apr in val.items():
                if pair.isupper():
                    file = f'{PATH}/{platform}_{pair}_{measurement}'
                    # TODO if the previous data point is the same as now, log but don't store
                    with open(f"{file}.csv", 'a') as data:
                        wr = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        wr.writerow([start, stop, apr])
        logger.info("query successful")
        
    except requests.exceptions.ConnectionError as e:
        logger.error(f"{type(e)}, {e}")
        return
        


def trigger_collection(token, sc):
    collect_data(token)
    s.enter(seconds, 1, trigger_collection, argument=(token, seconds,))
    s.run()


if __name__ == "__main__":
    # os.makedirs(PATH, exist_ok=True) # should exist already because of the Docker setup
    s = sched.scheduler(time.time, time.sleep)

    try:
        seconds = int(sys.argv[1])
    except IndexError as e:
        seconds = INTERVAL

    trigger_collection(TOKEN, seconds)