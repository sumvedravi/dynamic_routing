from config import *
from onos_interface import *
from onos_topo import *
from time import sleep


from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.shortest_paths.generic import shortest_path
from networkx.algorithms.shortest_paths.generic import all_shortest_paths


# if new flow add to flow_paths so that the list of device_id's and flow_ids can be appended to
# using this list of flow_ids the flows per device can be deleted and a new path with new flows can be added per device
def check_flows(stats, flow_paths):
	flows_dict = get_flows()
	for device_flow in flows_dict:
		for flow in device_flow['flows']:
			flow_id = flow['id']
			instruction_type = flow['treatment']['instructions'][0]['type']

			if instruction_type != 'OUTPUT':
				continue

			flow_treatment_inst = flow['treatment']['instructions'][0]['port']
			

			if flow_treatment_inst == 'CONTROLLER':
				continue

			device_id = flow['deviceId']
			src_mac = flow['selector']['criteria'][2]['mac']
			dst_mac = flow['selector']['criteria'][1]['mac']

			src_port = int(flow['selector']['criteria'][0]['port'])
			dst_port = int(flow_treatment_inst)

			pktRx = int(stats[device_id][src_port]['pktRx'])

			if src_mac not in flow_paths.keys():
				flow_paths[src_mac] = {}
		
			if dst_mac not in flow_paths[src_mac].keys():
				flow_paths[src_mac][dst_mac] = {}
				flow_paths[src_mac][dst_mac]['path'] = []
				flow_paths[src_mac][dst_mac]['flow_ids'] = {}				
				flow_paths[src_mac][dst_mac]['last_changed_sum'] = -1

			if device_id not in flow_paths[src_mac][dst_mac]['flow_ids'].keys():
				flow_paths[src_mac][dst_mac]['flow_ids'][device_id] = {}
				flow_paths[src_mac][dst_mac]['flow_ids'][device_id]['pktRx'] = 0
				flow_paths[src_mac][dst_mac]['flow_ids'][device_id]['last_changed'] = -1
			
			# increment count if no change, else decrement (until 0)	
			if pktRx == flow_paths[src_mac][dst_mac]['flow_ids'][device_id]['pktRx']:
				flow_paths[src_mac][dst_mac]['flow_ids'][device_id]['last_changed'] += 1
				flow_paths[src_mac][dst_mac]['last_changed_sum'] += 1
			else:
				last_changed = flow_paths[src_mac][dst_mac]['flow_ids'][device_id]['last_changed']
				last_changed_sum = flow_paths[src_mac][dst_mac]['last_changed_sum'] 

				flow_paths[src_mac][dst_mac]['flow_ids'][device_id]['last_changed'] = \
					max(last_changed - 1, 0)
				flow_paths[src_mac][dst_mac]['last_changed_sum'] -= \
					max(last_changed_sum - 1, 0)
				

			flow_paths[src_mac][dst_mac]['flow_ids'][device_id]['pktRx'] = pktRx
			flow_paths[src_mac][dst_mac]['flow_ids'][device_id]['flow_id'] = flow_id 


# grab all new intermediate flow ids for a specific connection between src_host and dst_host
# function is obsolete -- check_flows() handles this info gathering in next run of check_flows()
def get_new_flow_ids(src_mac, dst_mac, flow_paths):
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

			flow_paths[src_mac][dst_mac]['flow_ids'][device_id] = flow_id

# for src_host to dst_host connection add all intermediate flows 
# function works recursively ... resets path to [] once done
def add_all_flows(src_mac, dst_mac, path, links):
	if len(path) < 3:
		path.clear()
		return None

	# dev is the device the flow is being installed on
	src_dev = path[0]
	dev = path[1]
	dst_dev = path[2]

	# for device what port does data come in from link and what port does it go out		
	in_port = links[src_dev][dev]['dst_port']
	out_port = links[dev][dst_dev]['src_port']
	
	add_flow(dev, src_mac, dst_mac, in_port, out_port)
	
	path.remove(src_dev)
	add_all_flows(src_mac, dst_mac, path, links)


# for src_host to dst_host connection delete all intermediate flows 
# resets path parameter for connection to none		
def delete_all_flows(src_mac, dst_mac, flow_paths):
	for device_id in list(flow_paths[src_mac][dst_mac]['flow_ids'].keys()):
		device_data = flow_paths[src_mac][dst_mac]['flow_ids'][device_id]
		flow_id = device_data['flow_id']
		delete_flow(device_id, flow_id)
		#flow_paths[src_mac][dst_mac]['path'] = []
		del flow_paths[src_mac][dst_mac]['flow_ids'][device_id]
# for all src_host to dst_host connections delete all intermediate flows
# delte all src_host to dst_host connections in flow_paths
def delete_all_connections(flow_paths):
	for src_mac in list(flow_paths.keys()):
		for dst_mac in list(flow_paths[src_mac].keys()):
			delete_all_flows(src_mac, dst_mac, flow_paths)
			#del flow_paths[src_mac][dst_mac]
		#del flow_paths[src_mac]

# (1) update flow paths - get new flows if any 
# (2) check if any path has 'died' - if yes then delete all associated flows per device
# (3) check if any connection (src_host to dst_host) has a better path now
# 	(a) if yes then delete all old flows per device
#	(b) then add all new flows per device
#	(c) get new flow ids that have been assigned in previous step
def dynamic_routing(links, flow_paths, graph):
	# must check_flow() prior to running this function

	# a new flow will automatically use new_path since old_path will be = []
	# for each existing flow check if there is a new better path if so change to that
	for src_mac in list(flow_paths.keys()):
		for dst_mac in list(flow_paths[src_mac].keys()):
			last_changed_sum = flow_paths[src_mac][dst_mac]['last_changed']

			print('{} : {} - last_changed: {}'.format(src_mac, dst_mac, last_changed_sum))

			if last_changed_sum > 20:
				delete_all_flows(src_mac, dst_mac, flow_paths)
				del flow_paths[src_mac][dst_mac] # must remove full connection from list
				continue

			new_path = shortest_path(graph, src_mac, dst_mac, weight = 'weight')
			old_path = flow_paths[src_mac][dst_mac]['path']

			if new_path != old_path:						
				flow_paths[src_mac][dst_mac]['path'] = new_path
				delete_all_flows(src_mac, dst_mac, flow_paths)
				add_all_flows(src_mac, dst_mac, new_path.copy(), links)		
				print('new path for {} to {}: \n\t{} \n\t{}'.format(\
					src_mac, dst_mac, new_path, old_path))


