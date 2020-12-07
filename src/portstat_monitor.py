from config import *
from onos_interface import *
from onos_topo import *
from time import sleep

import sys, re, os
import subprocess
import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint


def check_portstats(links):
	stats = get_stats()
	# get max bw per links
	
	# file merge
	os.system('cat ../log/link_delay_* > ../log/link_delay.log')
	
	for src_dev in stats:
		for src_port in stats[src_dev]:	
			curr_bw = (stats[src_dev][src_port]['bytesRx'] + \
				stats[src_dev][src_port]['bytesTx']) * 8 / 1000 / 1000
			for dst_dev in links[src_dev]:
				if links[src_dev][dst_dev]['src_port'] == src_port:
					bw_per_sec = curr_bw - links[src_dev][dst_dev]['bw_before']
					links[src_dev][dst_dev]['bw_before'] = curr_bw
					links[src_dev][dst_dev]['bw'] = bw_per_sec
					if dst_dev[0:2] != 'of':
						links[dst_dev][src_dev]['bw_before'] = curr_bw
						links[dst_dev][src_dev]['bw'] = bw_per_sec
	
					# get delay	
					# helper script : link_check_delay.py h1 s1
					for line in reversed(list(open("../log/link_delay.log"))):
						#print(line.rstrip(), " each line")
						line = line.rstrip()
						line_src_dev = line.split(" ")[0]
						line_dst_dev = line.split(" ")[1]
						line_delay = line.split(" ")[2]
						# device and switch should be no more than 10.
						if line_src_dev[0:1] == 's':
							line_src_dev = 'of:000000000000000' + line_src_dev[1:2]
						else:
							line_src_dev = '00:00:00:00:00:0' + line_src_dev[1:2]
						if line_dst_dev[0:1] == 's':
							line_dst_dev = 'of:000000000000000' + line_dst_dev[1:2]
						else:
							line_dst_dev = '00:00:00:00:00:0' + line_dst_dev[1:2]
						if line_src_dev == src_dev and line_dst_dev == dst_dev:
							links[dst_dev][src_dev]['delay'] = line_delay
							links[src_dev][dst_dev]['delay'] = line_delay

