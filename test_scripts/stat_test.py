from config import *

import os
import json
import logging
import subprocess 
import requests as rq
import matplotlib.pyplot
from pprint import pprint
from requests.auth import HTTPBasicAuth


# testing REST API for statistics
#get_url = 'http://%s:%d/onos/v1/imr/imr/intentStats' % (ONOS_IP, ONOS_PORT)
#reply = rq.get(get_url, auth = HTTPBasicAuth(ONOS_USER, ONOS_PASS))
#print(reply.text)#.json()


# Testing CLI interface for portstats command

o = 'onos'
ip = '172.17.0.5'
cmd = 'portstats'
out = subprocess.Popen([o, ip, cmd, '-j'], \
			stdout=subprocess.PIPE, \
			stderr=subprocess.STDOUT)
stdout, stderr = out.communicate()

res = stdout.decode('utf-8')
print(res)

stats = {}
last_device = ''
last_port = None
for sub_str in res.split():
	check_if_device = sub_str[:8]
	check_if_port = sub_str[:4]
	check_if_Rx = sub_str[:5]
	check_if_Tx = sub_str[:5]
	check_if_bRx = sub_str[:7]
	check_if_bTx = sub_str[:7]
	check_if_Rxd = sub_str[:8]
	check_if_Txd = sub_str[:8]
	check_if_dur = sub_str[:3]

	if check_if_device == 'deviceId':
		stats[sub_str[9:]] = {}
		last_device = sub_str[9:]
	elif check_if_port == 'port':
		port_num = int(sub_str[5:].split(',')[0])
		stats[last_device][port_num] = {}
		last_port = port_num
	elif check_if_Rxd == 'pktRxDrp':
		val = int(sub_str[9:].split(',')[0])
		stats[last_device][last_port]['pktRxDrp'] = val
	elif check_if_Txd == 'pktTxDrp':
		val = int(sub_str[9:].split(',')[0])
		stats[last_device][last_port]['pktTxDrp'] = val
	elif check_if_Rx == 'pktRx':
		val = int(sub_str[6:].split(',')[0])
		stats[last_device][last_port]['pktRx'] = val
	elif check_if_Tx == 'pktTx':
		val = int(sub_str[6:].split(',')[0])
		stats[last_device][last_port]['pktTx'] = val
	elif check_if_bRx == 'bytesRx':
		val = int(sub_str[8:].split(',')[0])
		stats[last_device][last_port]['bytesRx'] = val
	elif check_if_bTx == 'bytesTx':
		val = int(sub_str[8:].split(',')[0])
		stats[last_device][last_port]['bytesTx'] = val
	elif check_if_dur == 'Dur':
		val = int(sub_str[4:].split(',')[0])
		stats[last_device][last_port]['Dur'] = val


pprint(stats)