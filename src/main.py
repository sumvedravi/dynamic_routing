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


def init_topology(devices, links, graph):
	links_dict = get_links()
	for link in links_dict:
		dst_dev = link['dst']['device']
		dst_port = int(link['dst']['port'])
		src_dev = link['src']['device']
		src_port = int(link['src']['port'])

		devices.append(src_dev)
		links.append((src_dev, src_port, dst_dev, dst_port))
	
	devices = list(set(devices))
	links= list(set(links))

	for device in devices:
		graph.add_node(device, type='device')

	for link in links:
		graph.add_edge(link[0], link[2], weight = 1.0) #can add weight based on delay
	
def draw_topo(graph, block=True):
	plt.figure()
	nx.draw(graph)
	plt.show()


if __name__ == '__main__':
	devices = [] 	#format [dev1, dev2, ...]
	links = [] 	#format [(src device , src port (int), dst device, dst port (int)), ...]
	graph = nx.Graph()

	
	init_topology(devices, links, graph)
	print(devices)
	print('----------------')
	print(links)
	draw_topo(graph)




