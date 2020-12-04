import csv
import os
import sched
import sys
import time

import requests


INTERVAL = 60
PATH = "/data/"
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjMyNDU2MSIsIm5hbWUiOiJNaXJvc2xhdiIsImlhdCI6Nzg5NDUyMTIzNTZ9.GQ5LR3jdhmTl_rmKgNPzrgNRrx9nflhJBiEgjz5Coec'
API_URL = "http://orcadefi.com:10000/api/v1/realtime/"
# API_URL = "http://orcadefi.com/api/v1/public/"

s = sched.scheduler(time.time, time.sleep)


def get_response_defi(query):
    try:
        response = requests.get(url=query)
        return response.json()
    except requests.exceptions.ConnectionError as e:
        print(f"{type(e)}, {e}")


def collect_data(token):
    query = f"{API_URL}all?token={token}"

    platforms = get_response_defi(query)

    for key_platform, val in platforms.items():
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


def trigger_collection(token, sc):
    collect_data(token)
    s.enter(sc, 1, trigger_collection, argument=(token, sc,))
    s.run()


if __name__ == "__main__":
    os.makedirs(PATH, exist_ok=True)

    try:
        sc = int(sys.argv[1])
    except IndexError as e:
        sc = INTERVAL

    trigger_collection(TOKEN, sc)