from config import *
from onos_interface import *
from onos_topo import *
from time import sleep


import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.shortest_paths.generic import shortest_path
from networkx.algorithms.shortest_paths.generic import all_shortest_paths


flow_id_list = []


# if new flow add to flow_paths so that the list of device_id's and flow_ids can be appended to
# using this list of flow_ids the flows per device can be deleted and a new path with new flows can be added per device
def check_flows(flow_paths):
	new_flows = {}
	flows_dict = get_flows()
	for device_flow in flows_dict:
		for flow in device_flow['flows']:
			flow_id = flow['id']
			flow_treatment_inst = flow['treatment']['instructions'][0]['port']
			
			if flow_treatment_inst == 'CONTROLLER':
				continue

			device_id = flow['deviceId']
			packets = int(flow['packets'])
			src_mac = flow['selector']['criteria'][2]['mac']
			dst_mac = flow['selector']['criteria'][1]['mac']

			if src_mac not in flow_paths.keys():
				flow_paths[srcmac_] = {}
		
			if dst_mac not in flow_paths[srcmac_].keys():
				flow_paths[src_mac][dst_mac] = {}
				flow_paths[src_mac][dst_mac]['path'] = []
				flow_paths[src_mac][dst_mac]['path_efficency'] = []
				flow_paths[src_mac][dst_mac]['flow_ids'] = {}
				flow_paths[src_mac][dst_mac]['last_changed'] += 1

			if device_id not in flow_paths[src_mac][dst_mac]['flow_ids'].keys():
				flow_paths[src_mac][dst_mac]['flow_ids'][device_id] = {}
				flow_paths[src_mac][dst_mac]['flow_ids'][device_id]['packets'] = packets
				flow_paths[src_mac][dst_mac]['flow_ids'][device_id]['last_changed'] = -1

			if packets == flow_paths[src_mac][dst_mac]['flow_ids'][device_id]['packets']:
				flow_paths[src_mac][dst_mac]['flow_ids'][device_id]['last_changed'] += 1
				flow_paths[src_mac][dst_mac]['last_changed'] += 1

			flow_paths[src_mac][dst_mac]['flow_ids'][device_id]['flow_id'] = flow_id 
			
	return new_flows

# grab all new intermediate flow ids for a connection between 
def get_new_flow_ids(src_mac, dst_mac, flow_paths)
	flows_dict = get_flows()
	for device_flow in flows_dict:
		for flow in device_flow['flows']:
			flow_treatment_inst = flow['treatment']['instructions'][0]['port']
			
			if flow_treatment_inst == 'CONTROLLER':
				continue

			src = flow['selector']['criteria'][2]['mac']
			dst = flow['selector']['criteria'][1]['mac']
			
			if src != src_mac or dst != dst_mac:
				continue

			flow_id = flow['id']
			device_id = flow['deviceId']

			flow_id_list.append(flow_id)
			flow_paths[src_mac][dst_mac]['flow_ids'][device_id] = flow_id

# for src_host to dst_host connection add all intermediate flows 
# function works recursively	
def add_all_flows(src_mac, dst_mac, path, links):
	if len(path) < 3:
		return None

	src_dev = path[i]
	dev = path[i+1]
	dst_dev = path[i+2]

	# for device what port does data come in from link and what port does it go out		
	in_port = links[src_dev][dev]['dst_port']
	out_port = links[dev][dst_dev]['src_port']
	
	add_flow(src_mac, dst_mac, in_port, out_port)
	
	path.remove(src_dev)
	add_all_flow(src_mac, dst_mac, path)


# for src_host to dst_host connection delete all intermediate flows 		
def delete_all_flows(src_mac, dst_mac, flow_paths):
	for device_id in flow_paths[src_mac][dst_mac]['flow_ids'].keys():
		device_data = flow_paths[src_mac][dst_mac]['flow_ids'].pop(device_id)
		flow_id = device_data['flow_id']
		flow_id_list.remove(flow_id)
		delete_flow(device_id, flow_id)

# for all src_host to dst_host connections delete all intermediate flows
def reset_flows(flow_paths):
	for src_mac in flow_paths.keys():
		for dst_mac in flow_paths[src_mac].keys():
			delete_all_flows(src_mac, dst_mac, flow_paths)

# (1) update flow paths - get new flows if any 
# (2) check if any path has 'died' - if yes then delete all associated flows per device
# (3) check if any connection (src_host to dst_host) has a better path now
# 	(a) if yes then delete all old flows per device
#	(b) then add all new flows per device
#	(c) get new flow ids that have been assigned in previous step
def dynamic_routing(flow_paths, links, graph):
	check_flows(flow_paths)
	
	# a new flow will automatically use new_path since old_path will be = []
	# for each existing flow check if there is a new better path if so change to that
	for src_mac in flow_paths.keys():
		for dst_mac in flow_paths[src_mac].keys():
			last_changed_sum = flow_paths[src_mac][dst_mac]['last_changed']

			if last_changed_sum > 20:
				delete_all_flows(src_mac, flow_paths)
				del flow_paths[src_mac][dst_mac] # must remove full connection from list
				continue

			new_path = shortest_path(graph, src_mac, dst_mac, weight = 'weight')
			old_path = flow_paths[src_mac][dst_mac]['path']

			if new_path != old_path:
				print('new path for {} to {}: {}'.format(src_mac, dst_mac, new_path)
				flow_paths[src_mac][dst_mac]['path'] = new_path
				delete_all_flows(src_mac, dst_mac, flow_paths)
				add_all_flows(src_mac, dst_mac, new_path)
				get_new_flow_ids(src_mac, dst_mac, flow_paths)
