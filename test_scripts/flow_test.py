from config import *

import os
import json
import logging
import subprocess 
import requests as rq
import matplotlib.pyplot
from pprint import pprint
from requests.auth import HTTPBasicAuth

# Testing CLI interface for get-flow-stats command
#cmd = 'get-flow-stats'
#deviceId = 'of:0000000000000003/2'
#out = subprocess.Popen([o, ip, cmd, deviceId,], \
#			stdout=subprocess.PIPE, \
#			stderr=subprocess.STDOUT)
#stdout, stderr = out.communicate()

#res = str(stdout.decode('utf-8')) 
#res_json = json.dumps(res)
#print(res_json)



o = 'onos'
ip = '172.17.0.5'
cmd = 'flows'
out = subprocess.Popen([o, ip, cmd, '-j',], \
			stdout=subprocess.PIPE, \
			stderr=subprocess.STDOUT)
stdout, stderr = out.communicate()

res = stdout.decode('utf-8')
res = res.replace("true", "True")
res = res.replace("false", "False")

res_dict = eval(res)
pprint(res_dict[0])
