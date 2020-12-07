from config import *
from onos_interface import *
from onos_topo import *
from time import sleep


import networkx as nx
import matplotlib.pyplot as plt


def flow_check(flow_paths):
	flows_dict = get_flows()

	for device_flow in flows_dict:
		device_id = device_flow['device']
		flow_count = device_flow['flowCount']

		if device_id not in flow_paths.keys():
			flow_paths[device_id] = {}

		flow_paths[device_id]['dev_flow_count'] = flow_count

		for flow in device_flow['flows']:
			# validation add
			if 'port' not in flow['treatment']['instructions'][0] or \
				'type' not in flow['treatment']['instructions'][0]:
				continue

			flow_id = flow['id']
			flow_treatment_inst = flow['treatment']['instructions'][0]['port']
			if flow_treatment_inst == 'CONTROLLER':
				continue

			port_ = flow['selector']['criteria'][0]['port']
			type_ = flow['selector']['criteria'][0]['type']
			srcmac_ = flow['selector']['criteria'][2]['mac']
			dstmac_ = flow['selector']['criteria'][1]['mac']
			treatmentport_ = flow['treatment']['instructions'][0]['port']
			treatmenttype_ = flow['treatment']['instructions'][0]['type']


			if srcmac_ not in flow_paths.keys():
				flow_paths[srcmac_] = {}
			
			if dstmac_ not in flow_paths[srcmac_].keys():
				flow_paths[srcmac_][dstmac_] = {}
				flow_paths[srcmac_][dstmac_]['active'] = True
				flow_paths[srcmac_][dstmac_]['path_index'] = -1
				flow_paths[srcmac_][dstmac_]['paths'] = []
				flow_paths[srcmac_][dstmac_]['path_values'] = []
				flow_paths[srcmac_][dstmac_]['flow_ids'] = []

			flow_paths[srcmac_][dstmac_]['flow_ids'].append( (device_id, flow_id))

	return flow_paths


'''
def flow_check():
	#format [(dev id, flow id, port no, type, src mac, dst mac, out port, out type), ...]
	pre_flows = []		
	while True:
		flows = []
		flows_dict = get_flows()
		#pprint(flows_dict)

		for device_flow in flows_dict:
			device_id = device_flow['device']
			flow_count = device_flow['flowCount']
			#print(device_id, flow_count)
			for flow in device_flow['flows']:
				flow_id = flow['id']
				flow_treatment_inst = flow['treatment']['instructions'][0]['port']
				if flow_treatment_inst != 'CONTROLLER':
					port_ = flow['selector']['criteria'][0]['port']
					type_ = flow['selector']['criteria'][0]['type']
					srcmac_ = flow['selector']['criteria'][2]['mac']
					dstmac_ = flow['selector']['criteria'][1]['mac']
					treatmentport_ = flow['treatment']['instructions'][0]['port']
					treatmenttype_ = flow['treatment']['instructions'][0]['type']

					flows.append( (device_id, flow_id, port_, type_, srcmac_, dstmac_, \
						treatmentport_, treatmenttype_) )
		#pprint(flows)
		# Check Flows (signal if new flow added)
		if pre_flows:
			for flow in flows:
				#print("current flows")
				flow_id = flow[1]
				#print(flow)
				check = 0
				for pre_flow in pre_flows:
					pre_flow_id = pre_flow[1]
					if flow_id == pre_flow_id:
						check = 1
				if check == 0:
					# add more logic to determine how to handle new flow
					print("new flow add")

		pre_flows = flows
		#print(prev_flows)
		sleep(1)
'''
