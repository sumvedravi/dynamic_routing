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
	#hosts = [] 	#format	[host1 mac, host2 mac, ...] 
	#devices = [] 	#format [dev1 id, dev2 id, ...]
	#links = [] 	#format [(src device , src port (int), dst device, dst port (int), status(1 up, 0 down)), ...]
	#graph = nx.Graph()
	
	#print(get_flows())
	init_topo(hosts, devices, links, graph)
	
	flow_paths = flow_check(flow_paths)

	#pprint(links)
		
	#print('************************************************************************')
	#print('************************************************************************')

	#pprint(flow_paths)

	draw_topo(graph, hosts, devices)

	while True:
		#portstat_check(hosts, devices, links, graph)
		#flow_check(flow_paths)
		#link_check(links)
		#update_topo()
		#sleep(1)
		
		#check_links(links)
		#check_portstats() --> updates bw values
		#check_delays()
		
	
	


	'''while True:
		print("-----------------------------------------")
		print(" 1: update topology			")
		print(" 2: calculate route                      ")
		print("                                         ")
		print(" q: quit					")
		print("-----------------------------------------")

		inp = input('choose menu : ')
		if inp == '1':
			print("update_topo")
			update_topo(hosts, devices, links, graph)
		if inp == '2':
			print("cal_route")
			cal_route(hosts, devices, links, graph)
		if inp == 'q':
			break

	for link in links:
		print(link)
        '''



