import csv
import logging
import sched
import sys

import requests


logging.basicConfig(format='{asctime} - {name} - {levelname} - {message}', style='{')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


INTERVAL = 60
PATH = "/data/"
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjMyNDU2MSIsIm5hbWUiOiJNaXJvc2xhdiIsImlhdCI6Nzg5NDUyMTIzNTZ9.GQ5LR3jdhmTl_rmKgNPzrgNRrx9nflhJBiEgjz5Coec'
API_URL = "http://orcadefi.com:10000/api/v1/realtime/"


def collect_data():
    query = f"{API_URL}all?token={TOKEN}"

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
        

def collection_loop(seconds, scheduler=None):
    if scheduler is not None:
        scheduler.enter(seconds, 1, collection_loop, ([seconds, scheduler]))
        collect_data()
    elif scheduler is None:
        scheduler = sched.scheduler()
        scheduler.enter(seconds, 1, collection_loop, ([seconds, scheduler]))
        scheduler.run()


if __name__ == "__main__":
    try:
        seconds = int(sys.argv[1])
    except IndexError as e:
        seconds = INTERVAL

    collection_loop(seconds)