from config import *

import os
import json
import logging
import subprocess 
import requests as rq
import matplotlib.pyplot
from pprint import pprint
from requests.auth import HTTPBasicAuth


o = 'onos'
ip = '172.17.0.5'
cmd = 'devices'
out = subprocess.Popen([o, ip, cmd, '-j',], \
			stdout=subprocess.PIPE, \
			stderr=subprocess.STDOUT)
stdout, stderr = out.communicate()

res = stdout.decode('utf-8')
res = res.replace("true", "True")
res = res.replace("false", "False")

res_dict = eval(res)
pprint(res_dict)
