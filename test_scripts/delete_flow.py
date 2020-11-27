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
FLOWID = '92042317780586387'

get_url = 'http://%s:%d/onos/v1/flows/%s/%s' % (ONOS_IP, ONOS_PORT, DEVICEID, FLOWID)
reply = rq.delete(get_url, auth = HTTPBasicAuth(ONOS_USER, ONOS_PASS))
print(reply.text)