from config import *
from onos_interface import *
from onos_topo import *
from time import sleep


import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.shortest_paths.generic import shortest_path


flow_id_list = []

def flow_check(flow_paths):
	flows_dict = get_flows()

	for device_flow in flows_dict:
		device_id = device_flow['device']
		flow_count = device_flow['flowCount']

		if device_id not in flow_paths.keys():
			flow_paths[device_id] = {}

		flow_paths[device_id]['dev_flow_count'] = flow_count

		for flow in device_flow['flows']:
			flow_id = flow['id']
			flow_treatment_inst = flow['treatment']['instructions'][0]['port']

			if flow_id in flow_id_list:
				continue
			
			if flow_treatment_inst == 'CONTROLLER':
				continue

			flow_ids_list.append(flow_id)

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

			flow_paths[srcmac_][dstmac_]['flow_ids'].append( (device_id, flow_id) )
			

	return flow_paths




def get_shortest_paths(hosts, devices, links, graph):
	pre_short_path = {}
	while True:
		short_path = {}
		print("cal_route")
		#print(hosts, links, devices)
		print("number of node : ", graph.number_of_nodes())
		print("nx.edge : ", graph.edges())
		print("nx.edges(data=True) : ", graph.edges(data=True) )
		# h1 -> h2 path where?
		print("links :", links)
		print("hosts :", hosts)
		#print(graph.shortest_path(graph, hosts[0], hosts[1], weight='weight'))
		for hosti in hosts:
			for hostj in hosts:
				if hosti == hostj:
					continue
				# dict key format : src-dst
				dict_index = hosti + "-" + hostj
				short_path[dict_index] = shortest_path(graph, hosti, hostj, weight='weight')
				print(hosti, hostj, "shortest path : ", shortest_path(graph, hosti, hostj, weight='weight'))
				if pre_short_path and short_path[dict_index] != pre_short_path[dict_index]:
					print("update flow by using new shortest path")
					#delete the pre flow (src - dst)
					for i in range(0, len(pre_short_path[dict_index])):
						print("delete flow srt, dst : ", pre_short_path[dict_index][i], pre_short_path[dict_index][i+1])

					# add the new flow (src - dst)
					for i in range(0, len(short_path[dict_index])):
						print("add flow srt, dst : ", short_path[dict_index][i], short_path[dict_index][i+1])
		pre_short_path = short_path
		sleep(1)
		break


