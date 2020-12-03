import csv
import os
import sched
import sys
import time

import requests

PATH = "data/"
token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjMyNDU2MSIsIm5hbWUiOiJNaXJvc2xhdiIsImlhdCI6Nzg5NDUyMTIzNTZ9.GQ5LR3jdhmTl_rmKgNPzrgNRrx9nflhJBiEgjz5Coec'

s = sched.scheduler(time.time, time.sleep)

def get_response_defi(query):
	response = requests.get(url=query)
	# Response in format json
	return response.json()

def collect_data(token):
	print('ok')
	query = f"http://orcadefi.com:10000/api/v1/realtime/all?token={token}"

	platforms = get_response_defi(query)
	# Iterate for every platform
	for key_platform, val in platforms.items():
		
		# Iterate over every pair for each platform 
		platform = val['Platform']
		measurement = val['_measurement']
		start = val['_start']
		stop = val['_stop']

		for pair, apr in val.items():
			if pair.isupper():
				file = f'{PATH}/{platform}_{pair}_{measurement}'
				
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
    except Exception as e:
    	sc = 900

    trigger_collection(token, sc)

