from config import *
from onos_interface import *
from onos_topo import *
from time import sleep

import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint


def link_check(links):
	# down method : mininet> link s1 s2 down/up
	#print(links)
	link_count = 0
	for link in links:
		if link[0] == 'switch-switch':
			link_count = link_count + 1
	# check current links
	links_status = get_links()
	link_count_curr = len(links_status)
	#print(link_count, link_count_curr)
	if link_count > link_count_curr:
		print("link count is changed, call cal_route and reroute")
