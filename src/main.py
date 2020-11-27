from config import *
from onos_interface import *
from onos_topo import *

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

			

if __name__ == '__main__':
	hosts = [] 	#format	[host1 mac, host2 mac, ...] 
	devices = [] 	#format [dev1 id, dev2 id, ...]
	links = [] 	#format [(src device , src port (int), dst device, dst port (int)), ...]

	graph = nx.Graph()
	
	
	init_topo(hosts, devices, links, graph)
	draw_topo(graph, hosts, devices)

	for link in links:
		print(link)



