from config import *
from onos_interface import *
from onos_topo import *
from time import sleep


import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.shortest_paths.generic import shortest_path


def get_shortest_paths(hosts, devices, links, graph):
	pre_short_path = {}
	while True:
		short_path = {}
		print("cal_route")
		#print(hosts, links, devices)
		print("number of node : ", graph.number_of_nodes())
		print("nx.edge : ", graph.edges())
		print("nx.edges(data=True) : ", graph.edges(data=True) )
		# h1 -> h2 path where?
		print("links :", links)
		print("hosts :", hosts)
		#print(graph.shortest_path(graph, hosts[0], hosts[1], weight='weight'))
		for hosti in hosts:
			for hostj in hosts:
				if hosti == hostj:
					continue
				# dict key format : src-dst
				dict_index = hosti + "-" + hostj
				short_path[dict_index] = shortest_path(graph, hosti, hostj, weight='weight')
				print(hosti, hostj, "shortest path : ", shortest_path(graph, hosti, hostj, weight='weight'))
				if pre_short_path and short_path[dict_index] != pre_short_path[dict_index]:
					print("update flow by using new shortest path")
					#delete the pre flow (src - dst)
					for i in range(0, len(pre_short_path[dict_index])):
						print("delete flow srt, dst : ", pre_short_path[dict_index][i], pre_short_path[dict_index][i+1])

					# add the new flow (src - dst)
					for i in range(0, len(short_path[dict_index])):
						print("add flow srt, dst : ", short_path[dict_index][i], short_path[dict_index][i+1])
		pre_short_path = short_path
		sleep(1)
		break
