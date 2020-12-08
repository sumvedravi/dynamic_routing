from config import *
from onos_topo import *
from onos_interface import *


import networkx as nx
import matplotlib.pyplot as plt


def get_links_config():
	config_file = open('links.config', 'r')
	lines = config_file.readlines()

	links_config = []
	for line in lines:
		links_config.append(line.split()) #{dev type} {id} {dev type} {id} {bandwidth} {delay} 

	return links_config

# dev_types is a 2 value array [dev type1, dev type2] , options are 'h' for host and 's' for switch
# dev_id is a 2 value array [dev id1, dev id2]
# returns bandwidth and delay if match ... else returns None, None
def find_config_match(links_config, dev_types, dev_ids):
	dev1 = int(dev_ids[0][-2:])
	dev2 = int(dev_ids[1][-2:])

	for link in links_config:
		conf_dev1 = int(link[1])
		conf_dev2 = int(link[3])

		bandwidth = int(link[4])
		delay = int(link[5])

		types_match 	    = (link[0] == dev_types[0] and link[2] == dev_types[1])
		types_match_reverse = (link[0] == dev_types[1] and link[2] == dev_types[0])

		devs_match 	   = types_match and (dev1 == conf_dev1 and dev2 == conf_dev2)
		devs_match_reverse = types_match_reverse and (dev1 == conf_dev2 and dev2 == conf_dev1)

		if devs_match or devs_match_reverse:
			return bandwidth, delay

	return None, None


def init_topo(hosts, devices, links, graph):
	hosts_dict = get_hosts()
	devs_dict = get_devices()	
	links_dict = get_links()
	links_config = get_links_config()
	
	for host in hosts_dict:
		host_mac = host['mac']
		dst_dev = host['locations'][0]['elementId']
		dst_port = int(host['locations'][0]['port'] )

		bandwidth, delay = find_config_match(links_config, ['h', 's'], [host_mac, dst_dev])
		
		if host_mac not in links.keys():
			links[host_mac] = {}

		if dst_dev not in links[host_mac].keys():
			links[host_mac][dst_dev] = {}

		links[host_mac][dst_dev]['conn_type'] = 'h-s'
		links[host_mac][dst_dev]['status'] = 1
		links[host_mac][dst_dev]['max_bw'] = bandwidth
		links[host_mac][dst_dev]['bw'] = -1
		links[host_mac][dst_dev]['bw_before'] = -1
		links[host_mac][dst_dev]['delay'] = 1
		links[host_mac][dst_dev]['link_flow_count'] = -1
		links[host_mac][dst_dev]['bw_norm'] = -1
		links[host_mac][dst_dev]['delay_norm'] = -1
		links[host_mac][dst_dev]['efficency'] = -1
		links[host_mac][dst_dev]['src_port'] = -1
		links[host_mac][dst_dev]['dst_port'] = dst_port
		

		# add flip of link, originally h->s, now also adds s->h

		if dst_dev not in links.keys():
			links[dst_dev] = {}

		if host_mac not in links[dst_dev].keys():
			links[dst_dev][host_mac] = {}
		
		links[dst_dev][host_mac]['conn_type'] = 's-h'
		links[dst_dev][host_mac]['status'] = 1
		links[dst_dev][host_mac]['max_bw'] = bandwidth
		links[dst_dev][host_mac]['bw'] = -1
		links[dst_dev][host_mac]['bw_before'] = -1
		links[dst_dev][host_mac]['delay'] = 1
		links[dst_dev][host_mac]['link_flow_count'] = -1
		links[dst_dev][host_mac]['bw_norm'] = -1
		links[dst_dev][host_mac]['delay_norm'] = -1
		links[dst_dev][host_mac]['efficency'] = -1
		links[dst_dev][host_mac]['src_port'] = dst_port #switched for switch -> host connection
		links[dst_dev][host_mac]['dst_port'] = -1
				
			
		hosts.append(host_mac)
			

	for dev in devs_dict:
		dev_id = dev['id']
		devices.append(dev_id)

	for link in links_dict:
		dst_dev = link['dst']['device']
		dst_port = int(link['dst']['port'])
		src_dev = link['src']['device']
		src_port = int(link['src']['port'])

		bandwidth, delay = find_config_match(links_config, ['s', 's'], [src_dev, dst_dev])

		if src_dev not in links.keys():
			links[src_dev] = {}

		if dst_dev not in links[src_dev].keys():
			links[src_dev][dst_dev] = {}

		links[src_dev][dst_dev]['conn_type'] = 's-s'
		links[src_dev][dst_dev]['status'] = 1
		links[src_dev][dst_dev]['max_bw'] = bandwidth
		links[src_dev][dst_dev]['bw'] = -1
		links[src_dev][dst_dev]['bw_before'] = -1
		links[src_dev][dst_dev]['delay'] = 1
		links[src_dev][dst_dev]['link_flow_count'] = -1
		links[src_dev][dst_dev]['bw_norm'] = -1
		links[src_dev][dst_dev]['delay_norm'] = -1
		links[src_dev][dst_dev]['efficency'] = -1

		links[src_dev][dst_dev]['src_port'] = src_port
		links[src_dev][dst_dev]['dst_port'] = dst_port
		
	
	devices = list(set(devices))

	for host in hosts:
		graph.add_node(host, type='host')
	for device in devices:
		graph.add_node(device, type='device')

	for src_dev in links:
		for dst_dev in links[src_dev]:	
			graph.add_edge(src_dev, dst_dev, weight = 1.0) #can add weight based on delay
	
def draw_topo(graph, hosts, devices):
	pos = nx.fruchterman_reingold_layout(graph)

	plt.figure()
	nx.draw_networkx_nodes(graph, pos, nodelist=hosts, node_color='r')
	nx.draw_networkx_nodes(graph, pos, nodelist=devices, node_color='b')	
	nx.draw_networkx_edges(graph, pos)
	nx.draw_networkx_labels(graph, pos)
	plt.show()
