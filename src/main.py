from global_vars import *
from onos_interface import *
from onos_topo import *
from portstat_monitor import *
from routing_engine import *
from link_monitor import *

import time
import _thread
from threading import Thread

import os
import sys
import json
import logging
import subprocess
import networkx as nx
import requests as rq
from pprint import pprint
import matplotlib.pyplot as plt
from requests.auth import HTTPBasicAuth



if __name__ == '__main__':

	init_topo(hosts, devices, links, graph)
	draw_topo(graph, hosts, devices)


	# first pass cycle after pingall is called ... then wipe connections to wait
	# for new connections to come in
	check_link(links, graph)	
	stats = get_stats()
	check_portstats(stats, links, graph)
	check_flows(stats, flow_paths)
	delete_all_connections(flow_paths)

	
	try:
		while True:
			# check link up and down
			check_link(links, graph)

			# get port stats		
			stats = get_stats()

			# check delay and bw per link
			check_portstats(stats, links, graph)
		
			# check current flows 
			check_flows(stats, flow_paths)

			# update paths and flows
			dynamic_routing(links, flow_paths, graph)

			sleep(1)
	
	except KeyboardInterrupt:
		pprint(links)
		pprint('\n\n\n')
		pprint(flow_paths)