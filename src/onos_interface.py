from config import *

import time
import _thread

import os
import json
import logging
import subprocess 
import requests as rq
import matplotlib.pyplot
from pprint import pprint
from requests.auth import HTTPBasicAuth


# src_mac, dst_mac are strings 
# in_port, out_port are ints
def add_flow(src_mac, dst_mac, in_port, out_port, priority = 100, _print = False):
	data = { \
		'isPermanent': True, \
		'priority': priority, \
		'selector': {'criteria': [{'port': in_port, 'type': 'IN_PORT'},{'mac': dst_mac,'type': 'ETH_DST'}, {'mac': src_mac, 'type': 'ETH_SRC'}]}, \
		'treatment': {'deferred': [], 'instructions': [{'port': out_port, 'type': 'OUTPUT'}]} \
	}

	json_data = json.dumps(data)	
	reply = rq.post(get_url, auth = HTTPBasicAuth(ONOS_USER, ONOS_PASS), data = json_data)

	if _print:
		print(reply.text)

	return None

# device id must be in form 'of:00000000000000xx', where xx is the device number
# flow id, is of form: 92042317780586387 .. this id can be found from get_flows() output dict 
def delete_flow(device_id, flow_id, _print = False):

	DEVICEID = 'of:0000000000000001'
	FLOWID = '92042317780586387'

	get_url = 'http://%s:%d/onos/v1/flows/%s/%s' % (ONOS_IP, ONOS_PORT, device_id, flow_id)
	reply = rq.delete(get_url, auth = HTTPBasicAuth(ONOS_USER, ONOS_PASS))

	if _print:
		print(reply.text)

	return None

def get_hosts(_print = False):
	out = subprocess.Popen(['onos', ONOS_IP, 'hosts', '-j',], \
				stdout=subprocess.PIPE, \
				stderr=subprocess.STDOUT)
	stdout, stderr = out.communicate()

	res = stdout.decode('utf-8')
	res = res.replace("true", "True")
	res = res.replace("false", "False")
	
	res_dict = eval(res)
	if _print:
		pprint(res_dect)

	return res_dict

def get_devices(_print = False):
	out = subprocess.Popen(['onos', ONOS_IP, 'devices', '-j',], \
				stdout=subprocess.PIPE, \
				stderr=subprocess.STDOUT)
	stdout, stderr = out.communicate()

	res = stdout.decode('utf-8')
	res = res.replace("true", "True")
	res = res.replace("false", "False")

	res_dict = eval(res)
	if _print:
		pprint(res_dect)

	return res_dict


def get_links(_print = False):
	out = subprocess.Popen(['onos', ONOS_IP, 'links', '-j',], \
				stdout=subprocess.PIPE, \
				stderr=subprocess.STDOUT)
	stdout, stderr = out.communicate()

	res = stdout.decode('utf-8')
	res = res.replace("true", "True")
	res = res.replace("false", "False")

	res_dict = eval(res)
	if _print:
		pprint(res_dect)

	return res_dict

	
def get_flows(_print = False):

	out = subprocess.Popen(['onos', ONOS_IP, 'flows', '-j',], \
				stdout=subprocess.PIPE, \
				stderr=subprocess.STDOUT)
	stdout, stderr = out.communicate()

	res = stdout.decode('utf-8')
	res = res.replace("true", "True")
	res = res.replace("false", "False")

	res_dict = eval(res)
	if _print:
		pprint(res_dect)


def get_stats(_print = False):
	# for some reason they did not implement the json return functionality ... so the -j 
	# option for json output does not work. Returned string must be parsed manually

	out = subprocess.Popen(['onos', ONOS_IP, 'portstats', '-j'], \
				stdout=subprocess.PIPE, \
				stderr=subprocess.STDOUT)
	stdout, stderr = out.communicate()

	res = stdout.decode('utf-8')

	stats = {}
	last_device = ''
	last_port = -1
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

	if _print:
		pprint(res_dect)

	