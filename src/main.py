from config import *
from onos_interface import *

import time
import _thread

import os
import json
import logging
import subprocess
import networkx as nx
import requests as rq
from pprint import pprint
import matplotlib.pyplot as plt
from requests.auth import HTTPBasicAuth


def init_topology(hosts, devices, links, graph):
	hosts_dict = get_hosts()
	devs_dict = get_devices()	
	links_dict = get_links()
	
	for host in hosts_dict:
		host_mac = host['mac']
		dst_dev = host['locations'][0]['elementId']
		dst_port = int(host['locations'][0]['port'] )

		hosts.append(host_mac)
		links.append( ('host-to-dev', host_mac, -1, dst_dev, dst_port) )

	for dev in devs_dict:
		dev_id = dev['id']
		devices.append(dev_id)

	for link in links_dict:
		dst_dev = link['dst']['device']
		dst_port = int(link['dst']['port'])
		src_dev = link['src']['device']
		src_port = int(link['src']['port'])

		links.append( ('dev-to-dev', src_dev, src_port, dst_dev, dst_port) )
	
	devices = list(set(devices))
	links= list(set(links))

	for host in hosts:
		graph.add_node(host, type='host')
	for device in devices:
		graph.add_node(device, type='device')
	for link in links:
		graph.add_edge(link[1], link[3], weight = 1.0) #can add weight based on delay
	
def draw_topo(graph, hosts, devices):
	pos = nx.fruchterman_reingold_layout(graph)

	plt.figure()
	nx.draw_networkx_nodes(graph, pos, nodelist=hosts, node_color='r')
	nx.draw_networkx_nodes(graph, pos, nodelist=devices, node_color='b')	
	nx.draw_networkx_edges(graph, pos)
	nx.draw_networkx_labels(graph, pos)
	plt.show()

if __name__ == '__main__':
	hosts = [] 	#format	[host1 mac, host2 mac, ...] 
	devices = [] 	#format [dev1 id, dev2 id, ...]
	links = [] 	#format [(src device , src port (int), dst device, dst port (int)), ...]
	graph = nx.Graph()

	
	init_topology(hosts, devices, links, graph)

	print(hosts)
	print('----------------')
	print(devices)
	print('----------------')
	print(links)

	draw_topo(graph, hosts, devices)




