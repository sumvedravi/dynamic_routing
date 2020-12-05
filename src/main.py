# initial vars
from global_vars import *
from config import *

# onos interaction
from onos_topo import *
from onos_interface import *

# real-time monitoring
from link_monitor import *
from flow_monitor import *
from portstat_monitor import *

# dynamic route engine
from cal_route import *


import time
import _thread
from threading import Thread
import sys

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
	init_topo(hosts, devices, links, graph)
	draw_topo(graph, hosts, devices)

	t1 = Thread(target=flow_check)
	t1.start()
	t2 = Thread(target=portstat_check, args=(hosts, devices, links, graph))
	t2.start()
	


	while True:
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
        



