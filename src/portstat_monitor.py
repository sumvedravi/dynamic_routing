from config import *
from onos_interface import *
from onos_topo import *
from time import sleep


import networkx as nx
import matplotlib.pyplot as plt


def portstat_check(hosts, devices, links, graph):
	#format [(dev id, flow id, port no, type, src mac, dst mac, out port, out type), ...]
	print(links)
	while True:
		# get max bw per links
		# get current bw per links
		# 
		# get delay
		# is the delay value custom? or 

		sleep(1)

