from global_vars import *
from onos_interface import *
from onos_topo import *
from portstat_monitor import *
from routing_engine import *
from link_monitor import *
from flow_monitor import *

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

	flow_paths = flow_check(flow_paths)


	#print('************************************************************************')
	#print('************************************************************************')

	#pprint(flow_paths)

	#draw_topo(graph, hosts, devices)

	while True:
		# check link up and down
		#check_link(links, graph)
		
		# check delay and bw per link
		#check_portstats(links, graph)

		#flow_check(flow_paths)
		#update_topo()

		sleep(1)
