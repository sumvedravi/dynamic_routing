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
	check_portstats(links, graph)
	check_flows(flow_paths)
	delete_all_connections(flow_paths)


	while True:
		# check link up and down
		check_link(links, graph)
		
		# check delay and bw per link
		check_portstats(links, graph)
		
		# check current flows 
		check_flows(links, flow_paths)

		# update paths and flows
		dynamic_routing(flow_paths, links, graph)

		sleep(1)
