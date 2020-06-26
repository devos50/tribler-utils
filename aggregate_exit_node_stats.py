"""
Aggregate slot statistics on a single exit node.
"""
import json

import requests
import time
from requests.exceptions import ConnectionError

json_data = {}

process_ind = 1
while True:
    try:
        print("Fetching statistics of node %d..." % process_ind)
        response = requests.get("http://localhost:%d/debug/circuits/slots" % (45000 + process_ind))
    except ConnectionError:
        break

    json_data[process_ind] = response.json()
    process_ind += 1

json_data["time"] = int(round(time.time() * 1000))

with open("stats.txt", "a") as stats_file:
    stats_file.write(json.dumps(json_data) + "\n")
