from config import *
from onos_interface import *
from onos_topo import *
from time import sleep

import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint


def link_check(links, graph):
	# down method : mininet> link s1 s2 down/up
	curr_links_status = get_links()
	for src in links:
		# we assume that host link always up
		if src[0:2] != 'of':
			continue
		for dst in links[src]:
			# we assume that host link always up
			if dst[0:2] != 'of':
				continue
			link_check = 0
			for alive_link in curr_links_status:
				if alive_link['src']['device'] == src and \
					alive_link['dst']['device'] == dst:
					link_check = 1
			if links[src][dst]['status'] != link_check:
				links[src][dst]['status'] = link_check
				# link down case
				# 1 -> 0
				if link_check == 0 and graph.has_edge(src, dst):
					graph.remove_edge(src, dst)
				# link up case
				# 0 -> 1
				if link_check == 1 and not graph.has_edge(src, dst):
					graph.add_edge(src, dst, weight = 1.0)
