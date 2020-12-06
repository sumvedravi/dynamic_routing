from config import *
from onos_interface import *
from onos_topo import *
from time import sleep

import sys, re, os
import subprocess
import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint


def portstat_check(hosts, devices, links, graph):
	before_bw = 0
	#format [(dev id, flow id, port no, type, src mac, dst mac, out port, out type), ...]
	print(links)
	stats = get_stats()
	pprint(stats)
	# get max bw per links
	ind = -1
	# file merge
	os.system('cat ../log/link_delay_* > ../log/link_delay.log')
	
	for link in links:
		ind = ind + 1
		if (link[0] == 'switch-switch'):
			src_sw = 's' + re.findall('\d+', link[1])[0].lstrip('0') + '-' + str(link[2])
			dest_sw = 's' + re.findall('\d+', link[3])[0].lstrip('0') + '-' + str(link[4])
			max_bw = link[4] * 1000 * 1000
			#print(typeof(stats))
			curr_bw = (stats[link[1]][link[2]]['bytesRx'] + stats[link[1]][link[2]]['bytesTx']) / 8
			links[ind][7] = curr_bw / 1000000 - links[ind][7]

			# get delay
			for line in reversed(list(open("../log/link_delay.log"))):
				#print(line.rstrip(), " each line")
				line = line.rstrip()
				line_src_sw = line.split(" ")[0]
				line_dest_sw = line.split(" ")[1]
				line_delay = line.split(" ")[2]
				if line_src_sw == src_sw[1] and line_dest_sw == dest_sw[1]:
					print("match")
					links[ind][8] = line_delay
					break
			print(src_sw, dest_sw, max_bw, curr_bw, links[ind][8])

