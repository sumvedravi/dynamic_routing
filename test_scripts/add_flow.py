from config import *

import os
import json
import logging
import subprocess 
import requests as rq
import matplotlib.pyplot
from pprint import pprint
from requests.auth import HTTPBasicAuth


DEVICEID = 'of:0000000000000001'


# s1 -> s2
data = { \
	'isPermanent': True, \
	'priority': 100, \
	'selector': {'criteria': [{'port': 2, 'type': 'IN_PORT'},{'mac': '00:00:00:00:00:02','type': 'ETH_DST'}, {'mac': '00:00:00:00:00:01', 'type': 'ETH_SRC'}]}, \
	'treatment': {'deferred': [], 'instructions': [{'port': '1', 'type': 'OUTPUT'}]} \
}

# s2 -> s1
data2 = { \
	'isPermanent': True, \
	'priority': 100, \
	'selector': {'criteria': [{'port': 2, 'type': 'IN_PORT'},{'mac': '00:00:00:00:00:01','type': 'ETH_DST'}, {'mac': '00:00:00:00:00:02', 'type': 'ETH_SRC'}]}, \
	'treatment': {'deferred': [], 'instructions': [{'port': '1', 'type': 'OUTPUT'}]} \
}


# s1 -> h1
data3 = { \
	'isPermanent': True, \
	'priority': 100, \
	'selector': {'criteria': [{'port': 2, 'type': 'IN_PORT'},{'mac': '00:00:00:00:00:01','type': 'ETH_DST'}, {'mac': '00:00:00:00:00:02', 'type': 'ETH_SRC'}]}, \
	'treatment': {'deferred': [], 'instructions': [{'port': '1', 'type': 'OUTPUT'}]} \
}

# s2 -> h2
data4 = { \
	'isPermanent': True, \
	'priority': 100, \
	'selector': {'criteria': [{'port': 2, 'type': 'IN_PORT'},{'mac': '00:00:00:00:00:01','type': 'ETH_DST'}, {'mac': '00:00:00:00:00:02', 'type': 'ETH_SRC'}]}, \
	'treatment': {'deferred': [], 'instructions': [{'port': '1', 'type': 'OUTPUT'}]} \
}

json_data = json.dumps(data)

get_url = 'http://%s:%d/onos/v1/flows/%s' % (ONOS_IP, ONOS_PORT, DEVICEID)
reply = rq.post(get_url, auth = HTTPBasicAuth(ONOS_USER, ONOS_PASS), data = json_data)
print(reply.text)